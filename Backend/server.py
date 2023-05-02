import socket
import databaseconn
import hashlib
import random
from datetime import *
import os
import json
import threading
# import base64

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

def handle_client(c, addr):
    try:
        print(f"[NEW CONNECTION] {addr} connected.")
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
                            otp = str(random.randint(100000, 999999))
                            response = {
                                'type': 'otp',
                                'otp': otp
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
                        query = "INSERT INTO users(name, email, phone, gender, bday, createdon, password) VALUES(%s, %s, %s, %s,%s, %s, %s)"
                        values= (request['name'], request['email'], request['phone'], request['gender'], request['bday'], createdon, hashed_password)
                        dbs_connection.insert(query,values)
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

                elif request['type'] == "login":
                    hashed_password = hashlib.sha256(request['password'].encode()).hexdigest()
                    try:
                        query = "SELECT id, name, email, password FROM users WHERE email = %s AND isdeleted= false"
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
                        query = "SELECT email,phone FROM users WHERE email = %s AND phone = %s AND isDeleted= false"
                        result = dbs_connection.search(query, (request['email'],request['phone']))
                        if not result:
                            response = {
                                'type': 'no_account'
                            }
                        else:
                            #OTP TO BE SENT VIA TWILIO (CODE PENDING)
                            otp = str(random.randint(100000, 999999))
                            response = {
                                'type': 'valid_account',
                                'otp': otp
                            }
                            print(f"OTP for {request['phone']} and {request['email']} is {otp}")
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
                        query = "UPDATE users SET password=%s WHERE email=%s AND phone=%s AND isDeleted= false"
                        values = (hashed_password, request['email'], request['phone'])
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

                elif request['type'] == "check_receipent":
                    try:
                        query = "SELECT id FROM users WHERE email = %s AND isDeleted= false"
                        result = dbs_connection.search(query, (request['receipentid'],))
                        if not result:
                            response = {
                                'type': 'no_receipent'
                            }
                        else:
                            receiverid = result[0][0]
                            response = {
                                'type': 'receipent_exists',
                                'receiverid':  receiverid
                            }
                    except BaseException as error:
                        print("Error: ", error)
                        response = {
                            'type': 'error'
                        }
                    finally:
                        send(c, response)

                elif request['type'] == "client_message":
                    try:
                        time = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
                        query = "INSERT INTO messages(time, sender, receiver, subject, message) VALUES(%s, %s, %s, %s, %s)"
                        values= (time, request['sender'], request['receiver'], request['subject'], request['body'])
                        dbs_connection.insert(query,values)
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

                elif request['type'] == "request_inbox_message":
                    try:
                        query = """SELECT m.id, m.time, usen.name AS sendername, usen.email AS senderid, urec.name AS receivername, urec.email as receiverid, m.isstarbyrecv, m.subject,m.message FROM messages m 
                                JOIN users usen ON m.sender = usen.id
                                JOIN users urec ON m.receiver = urec.id
                                WHERE m.receiver = %s AND isdelbyrecv = false ORDER BY id DESC"""
                        
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
                        query = """SELECT m.id, m.time, usen.name AS sendername, usen.email AS senderid, urec.name AS receivername, urec.email as receiverid, m.isstarbysndr, m.subject,m.message FROM messages m 
                                JOIN users usen ON m.sender = usen.id
                                JOIN users urec ON m.receiver = urec.id
                                WHERE m.sender = %s AND isdelbysndr = false ORDER BY id DESC"""
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
                        query = """SELECT m.id AS msgid, m.time AS time, usen.name AS sendername, usen.email AS senderid,
                                    urec.name AS receivername, urec.email AS receiverid, s.label AS label, m.subject AS subject,
                                    m.message AS message
                                FROM starred s
                                    JOIN messages m ON s.messageid = m.id
                                    JOIN users usen ON m.sender = usen.id
                                    JOIN users urec ON m.receiver = urec.id
                                WHERE starredby=%s ORDER BY s.id DESC"""
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
                            query = "UPDATE messages SET isstarbyrecv=true WHERE id=%s"
                            values = (request['messageid'],)
                            action = dbs_connection.update(query,values)
                            if action:
                                query = "INSERT INTO starred(starredby, label, messageid) VALUES(%s, %s, %s)"
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
                            query = "UPDATE messages SET isstarbyrecv=false WHERE id=%s"
                            values = (request['messageid'],)
                            action = dbs_connection.update(query,values)
                            if action:
                                query = "DELETE FROM starred WHERE starredby=%s AND label=%s AND messageid=%s"
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
                            query = "UPDATE messages SET isstarbysndr=true WHERE id=%s"
                            values = (request['messageid'],)
                            action= dbs_connection.update(query,values)
                            if action:
                                query = "INSERT INTO starred(starredby, label, messageid) VALUES(%s, %s, %s)"
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
                            query = "UPDATE messages SET isstarbysndr=false WHERE id=%s"
                            values = (request['messageid'],)
                            action = dbs_connection.update(query,values)
                            if action:
                                query = "DELETE FROM starred WHERE starredby=%s AND label=%s AND messageid=%s"
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
                            query = "UPDATE messages SET isdelbyrecv=true WHERE id=%s"
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
                            query = "UPDATE messages SET isdelbysndr=true WHERE id=%s"
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
                    try:
                        import base64
                        query = "SELECT name, email, phone, bday, gender, createdon,picture FROM users WHERE id = %s AND isDeleted= false"
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
                    try:
                        filename = f"userimages\\{request['byusremail']}{request['file_type']}"
                        with open(filename, 'wb') as f:
                            f.write(image_bytes)
                        print("done")
                        query = "UPDATE users SET picture= %s WHERE id=%s"
                        values = (filename,request['byuserid'])
                        dbs_connection.update(query,values)
                        response = {
                            'type': 'image_changed'
                        }
                    except BaseException as msg:
                        response = {
                            'type': 'error'
                        }
                    finally:
                        send(c, response)                    
                        
                elif request['type'] == "delete_account":
                    hashed_password = hashlib.sha256(request['password'].encode()).hexdigest()
                    try:
                        query = "SELECT email, password FROM users WHERE email = %s AND password = %s and isDeleted= false"
                        result = dbs_connection.search(query, (request['email'],hashed_password))
                        if len(result) >0:
                            query = "UPDATE users SET isDeleted= true WHERE id=%s AND email=%s"
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
                        query = "SELECT password FROM users WHERE id= %s AND email = %s AND isDeleted=false"
                        result = dbs_connection.search(query, (request['byid'],request['email']))
                        stopwd = result[0]
                        if stopwd[0] != hashedcurr_password:
                            response = {
                                'type': 'wrong_password'
                            }
                        else:
                            query = "UPDATE users SET password=%s WHERE id=%s AND email=%s AND isDeleted=false"
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