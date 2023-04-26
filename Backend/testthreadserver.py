import socket
import databaseconn
import hashlib
import random
from datetime import *
import json
import threading

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
                    print(msg_length)
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
                        query = "SELECT email FROM user_data WHERE email = %s"
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
                    dates = datetime.now().date()
                    hashed_password = hashlib.sha256(request['password'].encode()).hexdigest()  
                    try:
                        query = "INSERT INTO user_data(fullname, email, phone, gender, bday,ageaccount,status, password) VALUES(%s, %s, %s,%s, %s, %s,%s, %s)"
                        values= (request['name'], request['email'], request['phone'], request['gender'], request['bday'],dates,"Active", hashed_password)
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
                        query = "SELECT fullname, email, password FROM user_data WHERE email = %s AND status = %s"
                        result = dbs_connection.search(query, (request['email'],'Active'))
                        if not result:
                            response = {
                                'type': 'no_account'
                            }
                        else:
                            usr_name, usr_email, usr_password = result[0]
                            if usr_password != hashed_password:
                                response = {
                                    'type': 'incorrect_password'
                                }
                            else:
                                response = {
                                    'type': 'login_success',
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
                        query = "SELECT email,phone FROM user_data WHERE email = %s AND phone = %s"
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
                        query = "UPDATE user_data SET password=%s WHERE email=%s AND phone=%s AND status= %s"
                        values = (hashed_password, request['email'], request['phone'], 'Active')
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
                        query = "SELECT fullname FROM user_data WHERE email = %s AND status = %s"
                        result = dbs_connection.search(query, (request['receipentid'],'Active'))
                        if not result:
                            response = {
                                'type': 'no_receipent'
                            }
                        else:
                            receivername = result[0][0]
                            response = {
                                'type': 'receipent_exists',
                                'receivername':  receivername
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
                        query = "INSERT INTO messages(time, sendername, senderid, receivername, receiverid, subject, message) VALUES(%s, %s, %s, %s, %s, %s, %s)"
                        values= (time, request['sendername'], request['senderid'], request['receivername'], request['receiverid'], request['subject'], request['body'])
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

                # elif request['type'] == "request_inbox_message":
                #     receiver = data[1]
                #     try:
                #         query = "SELECT *FROM messages where senderid= %s ORDER BY time DESC"
                #         result = dbs_connection.search(query, (receiver,))
                #         print(result)
                #         if not result:
                #             response = "empty_inbox"
                #         else:
                #             response = result
                #     except BaseException as msg:
                #             response= "error"
                #             print(msg)
                #     finally:
                #         c.send(json.dumps(response).encode())

                elif request['type'] == "view_profile":
                    try:
                        query = "SELECT fullname, email, phone, bday,gender, ageaccount FROM user_data WHERE email = %s"
                        result = dbs_connection.search(query, (request['email'],))
                        pname, pemail,pmob, pbday, pgen, pacc  = result[0]
                        response= {
                            'type': 'my_profile',
                            'name': pname,
                            'email': pemail,
                            'mobile': pmob,
                            'bday': pbday,
                            'gender': pgen,
                            'accountdate': pacc
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
                        query = "SELECT email, password FROM user_data WHERE email = %s AND password = %s"
                        result = dbs_connection.search(query, (request['email'],hashed_password))
                        if len(result) >0:
                            query = "UPDATE user_data SET fullname= NULL, phone= NULL, gender= NULL, bday=NULL, ageaccount= NULL, status='Inactive', password= NULL WHERE email= %s"
                            dbs_connection.update(query, (request['email'],))
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
                        query = "SELECT password FROM user_data WHERE email = %s"
                        result = dbs_connection.search(query, (request['email'],))
                        stopwd = result[0]
                        if stopwd[0] != hashedcurr_password:
                            response = {
                                'type': 'wrong_password'
                            }
                        else:
                            query = "UPDATE user_data SET password=%s WHERE email=%s"
                            values = (hashednew_password, request['email'])
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
