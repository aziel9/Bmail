import socket
import databaseconn
import hashlib
import random
from datetime import *
import json
import threading
from io import BytesIO
from PIL import Image
from randomnum import RandomPrime as rp
from randomnum import primitive as pr
import random
import requests
import geocoder
from twilio.rest import Client

HEADER = 1024
PORT = 1234
SERVER = "100.83.45.111"
ADDR = (SERVER, PORT)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(ADDR)
dbs_connection = databaseconn.DatabaseConnection()

def send(c, response):
    response_json = json.dumps(response).encode()
    response_len = len(response_json)
    send_length = response_len.to_bytes(4, byteorder='big')
    c.sendall(send_length)
    c.sendall(response_json)

def get_weather():
    g = geocoder.ip('me')
    latitude = g.lat
    longitude = g.lng

    api_url = 'https://api.open-meteo.com/v1/forecast'
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'current_weather': 'true',
    }
    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        data = response.json()
        current_temperature = data['current_weather']['temperature']
        return current_temperature
    else:
        print('Error:', response.status_code)

def send_sms(number):
    # account_sid = 'Cff1bf5163825150e9ffc1ce4a21dae0'
    # auth_token = 'e581185c5d6fd23521b836148d13aa'
    # client = Client(account_sid, auth_token)

    otp = str(random.randint(100000, 999999))
    # num = number
    # msg = f"Your OTP code for Bmail is {otp}"
    # message = client.messages \
    #                 .create(
    #                     body=msg,
    #                     from_='+15734754862',
    #                     to=num
    #                 )
    return otp

def handle_client(c, addr):
    global otp, P
    try:
        print(f"[NEW CONNECTION] {addr} connected.")
        temp= get_weather()
        connected = True
        while connected:
                msg_length_bytes = c.recv(4)
                if msg_length_bytes:
                    msg_length = int.from_bytes(msg_length_bytes, byteorder='big')
                    data = b''
                    while len(data) < msg_length:
                        chunk = c.recv(min(msg_length - len(data), 1024))
                        if not chunk:
                            break
                        data += chunk
                    request = json.loads(data.decode())
                    print(request)

                if request['type'] == "verify_signup":
                    email = request['email']
                    phone = request['phone']
                    try:
                        query = "SELECT email FROM users WHERE email = %s"
                        result = dbs_connection.search(query, (email,))
                        if result:
                            response = {
                                'type': 'email_exists'
                            }
                        else:
                            #OTP TO BE SENT VIA TWILIO (CODE PENDING)
                            otp = send_sms(phone)
                            response = {
                                'type': 'otp_sent',
                            }
                            print(f"OTP for {phone} and {email} is {otp}")
                    except BaseException as msg:
                        response = {
                            'type': 'otp_failed'
                        }
                        print(msg)
                    finally:
                        send(c, response)

                elif request['type'] == "signup":
                    createdon = datetime.now().date()
                    hashed_password = hashlib.sha256(request['password'].encode()).hexdigest()  
                    try:
                        query = "INSERT INTO users(name, email, password) VALUES(%s, %s, %s) RETURNING user_id"
                        values= (request['name'], request['email'], hashed_password)
                        result = dbs_connection.insert_return(query,values)
                        userid = result
                        query = "INSERT INTO users_info(user_id, phone, gender, bday, createdon) VALUES(%s,%s,%s,%s,%s)"
                        values = (userid, request['phone'], request['gender'], request['bday'], createdon)
                        dbs_connection.insert(query, values)
                        response = {
                            'type': 'signup_success'
                        }
                    except BaseException as error:
                        print("Error: ", error)
                        response = {
                            'type': 'signup_fail'
                        }
                    finally:
                        send(c, response)

                elif request['type'] == "validate_otp":
                    try: 
                        if request['otp'] == otp:
                            response = {
                                'type' : 'correct_otp'
                            }
                            otp = None
                        else:
                            response = {
                                'type' : 'incorrect_otp'
                            }
                    finally:
                        send(c, response)

                elif request['type'] == "login":
                    hashed_password = hashlib.sha256(request['password'].encode()).hexdigest()
                    try:
                        query = "SELECT user_id, name, email, password FROM users WHERE email = %s AND isdeleted= false"
                        result = dbs_connection.search(query, (request['email'],))
                        if not result:
                            response = {
                                'type': 'no_account'
                            }
                        else:
                            usr_id, usr_name, usr_email, usr_password = result[0]
                            if usr_password != hashed_password:
                                response = {
                                    'type': 'incorrect_password'
                                }
                            else:
                                response = {
                                    'type': 'login_success',
                                    'active_id': usr_id,
                                    'active_user': usr_name,
                                    'active_email':  usr_email
                                }

                    except BaseException as error:
                        print("Error: ", error)
                        response = {
                            'type': 'login_fail'
                        }
                    finally:
                        send(c, response)

                elif request['type'] == "forgot_password":
                    try:
                        query = "SELECT u.email, ui.phone FROM users u JOIN users_info ui ON u.user_id = ui.user_id WHERE u.email=%s AND ui.phone=%s AND u.isdeleted=false;"
                        result = dbs_connection.search(query, (request['email'],request['phone']))
                        email, phone = result[0]
                        print(phone)
                        if not result:
                            response = {
                                'type': 'no_account'
                            }
                        else:
                            otp = send_sms(phone)
                            response = {
                                'type': 'valid_account'
                                # 'otp': otp
                            }
                            print(f"OTP for {email} and {phone} is {otp}")
                    except BaseException as msg:
                        response = {
                            'type': 'error'
                        }
                        print(msg)
                    finally:
                        send(c, response)

                elif request['type'] == "change_password":
                    hashed_password = hashlib.sha256(request['password'].encode()).hexdigest()
                    try:
                        query = "UPDATE users SET password=%s WHERE email=%s AND isdeleted= false"
                        values = (hashed_password, request['email'])
                        dbs_connection.update(query,values)
                        response = {
                            'type': 'password_changed'
                        }
                    except:
                        response = {
                            'type': 'password_change_failed'
                        }
                    finally:
                        send(c, response)

                elif request['type'] == "home_info":
                    try:
                        query = "SELECT (SELECT COUNT(*) FROM emails WHERE receiver = %s), (SELECT COUNT(*) FROM emails WHERE sender = %s) ,(SELECT name FROM users WHERE user_id = %s)"
                        result = dbs_connection.search(query, (request['byid'],request['byid'], request['byid']))
                        received, sent, name = result[0]
                        fname = name.split()[0]
                        response = {
                            'type' : 'home_info',
                            'name' : fname,
                            'temperature' : int(temp),
                            'received' : received,
                            'sent' : sent
                        }
                    except BaseException as msg:
                        response = {
                            'type' : 'error'
                        }
                        print(msg)
                    finally:
                        send(c, response)

                elif request['type'] == "key_exchange":
                    if request['label'] == "generate_key":
                        try:
                            query = "SELECT user_id FROM users WHERE email = %s AND isdeleted= false"
                            result = dbs_connection.search(query, (request['receipentid'],))
                            if not result:
                                response = {
                                    'type': 'no_receipent'
                                }
                            else:
                                receiverid = result[0][0]
                                P = rp()
                                G = pr(P)
                                receiver_privatekey = random.choice(range(100))
                                receiver_publickey = pow(G,receiver_privatekey,P)
                                response = {
                                    'type': 'receipent_exists',
                                    'receiverid':  receiverid,
                                    'prime': P,
                                    'primitive': G,
                                    'receiver_publickey' : receiver_publickey
                                }
                        except BaseException as error:
                            print("Error: ", error)
                            response = {
                                'type': 'error'
                            }
                        finally:
                            send(c, response)

                    elif request['label'] == "store_key_and_message":
                        try:
                            sender_publickey = int(request['sender_publickey'])
                            shared_key = pow(sender_publickey,receiver_privatekey,P)
                            print(shared_key)  
                            time = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
                            query = "INSERT INTO emails(time, sender, receiver, subject, message, key) VALUES(%s, %s, %s, %s, %s, %s) RETURNING email_id"
                            values= (time, request['sender'], request['receiver'], request['subject'], request['body'],shared_key)
                            result = dbs_connection.insert_return(query,values)
                            email_id = result
                            query = "INSERT INTO email_status(email_id) VALUES(%s)"
                            dbs_connection.insert(query,(email_id,))
                            response = {
                                'type': 'message_sent'
                            }
                        except BaseException as error:
                            response = {
                                'type': 'message_sent_failed'
                            }
                            print(error)
                        finally:
                            send(c, response)
                            P = None

                elif request['type'] == "request_inbox_message":
                    try:
                        query = """SELECT e.email_id, e.time, usen.name, usen.email, urec.name, urec.email, es.isstarbyrecv, e.subject,e.message,e.key FROM emails e 
                                JOIN users usen ON e.sender = usen.user_id
                                JOIN users urec ON e.receiver = urec.user_id
                                JOIN email_status es ON e.email_id = es.email_id
                                WHERE e.receiver = %s AND es.isdelbyrecv = false ORDER BY e.email_id DESC"""
                        
                        result = dbs_connection.search(query, (request['byid'],))
                        if not result:
                            response = {
                                'type': 'empty_inbox'
                            }
                        else:
                            response = {
                                'type':  'inbox_found',
                                'inbox': result
                            }
                    except BaseException as msg:
                            response= {
                                'type': 'error'
                            }
                            print(msg)
                    finally:
                        send(c, response)

                elif request['type'] == "request_sentbox_message":
                    try:
                        query = """SELECT e.email_id, e.time, usen.name, usen.email, urec.name, urec.email, es.isstarbysndr, e.subject,e.message, e.key FROM emails e 
                                JOIN users usen ON e.sender = usen.user_id
                                JOIN users urec ON e.receiver = urec.user_id
                                JOIN email_status es ON e.email_id = es.email_id
                                WHERE e.sender = %s AND es.isdelbysndr = false ORDER BY email_id DESC"""
                        result = dbs_connection.search(query, (request['byid'],))
                        if not result:
                            response = {
                                'type': 'empty_sentbox'
                            }
                        else:
                            response = {
                                'type':  'sentbox_found',
                                'sentbox': result
                            }
                    except BaseException as msg:
                            response= {
                                'type': 'error'
                            }
                            print(msg)
                    finally:
                        send(c, response)

                elif request['type'] == "request_starredbox_message":
                    try:
                        query = """SELECT e.email_id, e.time, usen.name, usen.email,
                                    urec.name, urec.email, s.label, e.subject, e.message, e.key
                                FROM starred s
                                    JOIN emails e ON s.email_id = e.email_id
                                    JOIN users usen ON e.sender = usen.user_id
                                    JOIN users urec ON e.receiver = urec.user_id
                                WHERE starredby=%s ORDER BY s.starred_id DESC"""
                        result = dbs_connection.search(query, (request['byid'],))
                        if not result:
                            response = {
                                'type': 'empty_starredbox'
                            }
                        else:
                            response = {
                                'type':  'starredbox_found',
                                'starredbox': result
                            }
                    except BaseException as msg:
                            response= {
                                'type': 'error'
                            }
                            print(msg)
                    finally:
                        send(c, response)

                elif request['type'] == 'starring_message':
                    if request['label'] == 'star_inbox':
                        try:
                            query = "UPDATE email_status SET isstarbyrecv=true WHERE email_id=%s"
                            values = (request['messageid'],)
                            action = dbs_connection.update(query,values)
                            if action:
                                query = "INSERT INTO starred(starredby, label, email_id) VALUES(%s, %s, %s)"
                                values= (request['byuserid'], 'Inbox', request['messageid'])
                                dbs_connection.insert(query,values)
                            response = {
                                'type': 'message_starred_on_inbox'
                            }
                        except BaseException as msg:
                            response = {
                                'type': 'error'
                            }
                            print(msg)
                        finally:
                            send(c, response)

                    elif request['label'] == 'unstar_inbox':
                        try:
                            query = "UPDATE email_status SET isstarbyrecv=false WHERE email_id=%s"
                            values = (request['messageid'],)
                            action = dbs_connection.update(query,values)
                            if action:
                                query = "DELETE FROM starred WHERE starredby=%s AND label=%s AND email_id=%s"
                                values = (request['byuserid'], 'Inbox', request['messageid'])
                                dbs_connection.delete(query,values)
                            response = {
                                'type': 'message_unstarred_on_inbox'
                            }
                        except BaseException as msg:
                            response = {
                                'type': 'error'
                            }
                            print(msg)
                        finally:
                            send(c, response)

                    elif request['label'] == 'star_sent':
                        try:
                            query = "UPDATE email_status SET isstarbysndr=true WHERE email_id=%s"
                            values = (request['messageid'],)
                            action= dbs_connection.update(query,values)
                            if action:
                                query = "INSERT INTO starred(starredby, label, email_id) VALUES(%s, %s, %s)"
                                values= (request['byuserid'], 'Sent', request['messageid'])
                                dbs_connection.insert(query,values)
                            response = {
                                'type': 'message_starred_on_sent'
                            }
                        except BaseException as msg:
                            response = {
                                'type': 'error'
                            }
                            print(msg)
                        finally:
                            send(c, response)

                    elif request['label'] == 'unstar_sent':
                        try:
                            query = "UPDATE email_status SET isstarbysndr=false WHERE email_id=%s"
                            values = (request['messageid'],)
                            action = dbs_connection.update(query,values)
                            if action:
                                query = "DELETE FROM starred WHERE starredby=%s AND label=%s AND email_id=%s"
                                values = (request['byuserid'], 'Sent', request['messageid'])
                                dbs_connection.delete(query,values)
                            response = {
                                'type': 'message_unstarred_on_sent'
                            }
                        except BaseException as msg:
                            response = {
                                'type': 'error'
                            }
                            print(msg)
                        finally:
                            send(c, response)

                elif request['type'] == 'delete_message':
                    if request['label'] == 'inbox':
                        try:
                            query = "UPDATE email_status SET isdelbyrecv=true WHERE email_id=%s"
                            values = (request['messageid'],)
                            dbs_connection.update(query,values)
                            response = {
                                'type': 'message_deleted_from_inbox'
                            }
                        except BaseException as msg:
                            response = {
                                'type': 'error'
                            }
                            print(msg)
                        finally:
                            send(c, response)

                    elif request['label'] == 'sent':
                        try:
                            query = "UPDATE email_status SET isdelbysndr=true WHERE email_id=%s"
                            values = (request['messageid'],)
                            dbs_connection.update(query,values)
                            response = {
                                'type': 'message_deleted_from_sent'
                            }
                        except BaseException as msg:
                            response = {
                                'type': 'error'
                            }
                            print(msg)
                        finally:
                            send(c, response)

                elif request['type'] == "view_profile":
                    if request['label'] == "user_icon":
                        try:
                            import base64
                            query = "SELECT u.email, ui.picture FROM users u JOIN users_info ui ON u.user_id = ui.user_id WHERE u.user_id=%s"
                            result = dbs_connection.search(query, (request['byuserid'],))
                            uemail, iconfile =result[0]
                            if iconfile == "userimages\\default.png":
                                filename = "userimages\\icondefault.png"
                                with open(filename, 'rb') as f:
                                    icon_bytes = f.read()
                            else:
                                filename= iconfile.replace(f"{uemail}",f"icon{uemail}")
                                with open(filename, 'rb') as f:
                                    icon_bytes = f.read()
                            icon_bytes = base64.b64encode(icon_bytes).decode('utf-8')
                            response = {
                                'type': 'user_icon',
                                'file_byte': icon_bytes
                            }
                        except BaseException as msg:
                            response = {
                                'type': 'error'
                            }
                            print(msg)
                        finally:
                            send(c, response)

                    elif request['label'] == "myprofile":
                        try:
                            import base64
                            query = "SELECT u.name, u.email, ui.phone, ui.bday, ui.gender, ui.createdon, ui.picture FROM users u JOIN users_info ui ON u.user_id = ui.user_id WHERE u.user_id = %s AND u.isDeleted= false"
                            result = dbs_connection.search(query, (request['byid'],))
                            pname, pemail,pmob, pbday, pgen, pacc,pfile  = result[0]
                            with open(pfile, 'rb') as f:
                                img_bytes = f.read()
                            image_bytes = base64.b64encode(img_bytes).decode('utf-8')
                            response= {
                                'type': 'my_profile',
                                'name': pname,
                                'email': pemail,
                                'mobile': pmob,
                                'bday': pbday,
                                'gender': pgen,
                                'accountdate': pacc,
                                'file_byte': image_bytes
                            }
                        except BaseException as msg:
                            response = {
                                'type': 'error'
                            }
                            print(msg)
                        finally:
                            send(c, response)

                elif request['type'] == "change_picture":
                    import base64
                    image_bytes = base64.b64decode(request['file_byte'])
                    resize_icon = Image.open(BytesIO(image_bytes))
                    resize_image = resize_icon.resize((50, 50), resample=Image.LANCZOS)
                    try:
                        filename = f"userimages\\{request['byusremail']}.png"
                        iconname = f"userimages\\icon{request['byusremail']}.png"
                        with open(filename, 'wb') as f:
                            f.write(image_bytes)
                        with open(iconname, 'wb') as f:
                            resize_image.save(f)
                        query = "UPDATE users_info SET picture= %s WHERE user_id=%s"
                        values = (filename,request['byuserid'])
                        dbs_connection.update(query,values)
                        response = {
                            'type': 'image_changed'
                        }
                    except BaseException as msg:
                        response = {
                            'type': 'error'
                        }
                        print(msg)
                    finally:
                        send(c, response)                    
                        
                elif request['type'] == "delete_account":
                    hashed_password = hashlib.sha256(request['password'].encode()).hexdigest()
                    try:
                        query = "SELECT email, password FROM users WHERE email = %s AND password = %s and isDeleted= false"
                        result = dbs_connection.search(query, (request['email'],hashed_password))
                        if len(result) >0:
                            query = "UPDATE users SET isDeleted= true WHERE user_id=%s AND email=%s"
                            dbs_connection.update(query, (request['byid'],request['email']))
                            response = {
                                'type': 'delete_account_success'
                            }
                        else:
                            response = {
                                'type': 'wrong_password'
                            }
                    except BaseException as msg:
                        response = {
                            'type':  'error'
                        }
                        print(msg)
                    finally:
                        send(c, response)

                elif request['type'] == "update_password":
                    hashedcurr_password = hashlib.sha256(request['password'].encode()).hexdigest()
                    hashednew_password = hashlib.sha256(request['newpassword'].encode()).hexdigest()
                    try:
                        query = "SELECT password FROM users WHERE user_id= %s AND email = %s AND isDeleted=false"
                        result = dbs_connection.search(query, (request['byid'],request['email']))
                        stopwd = result[0]
                        if stopwd[0] != hashedcurr_password:
                            response = {
                                'type': 'wrong_password'
                            }
                        else:
                            query = "UPDATE users SET password=%s WHERE user_id=%s AND email=%s AND isDeleted=false"
                            values = (hashednew_password, request['byid'],request['email'])
                            dbs_connection.update(query,values)
                            response = {
                                'type': 'update_password_success'
                            }
                    except BaseException as error:
                        print("Error: ", error)
                        response = {
                            'type': 'error'
                        }
                    finally:
                        send(c, response)

    except ConnectionResetError:
        print(f"[DISCONNECTION] {addr} disconnected.")

    c.close()


def start():
    server_socket.listen(5)
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        c, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(c, addr))
        thread.dbs_connection = dbs_connection
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] Server is starting...")
start()