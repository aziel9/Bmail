import socket
import databaseconn
import hashlib
import random
import threading

def handle_connection(c, addr):
    dbs_connection = databaseconn.DatabaseConnection()

    data = c.recv(2048).decode()
    data = data.split("|")
    request_type = data[0]

    if request_type == "verify_signup":
        email = data[1]
        phone = data[2]
        try:
            query = "SELECT email FROM user_data WHERE email = %s"
            result = dbs_connection.search(query, (email,))
            if result != []:
                response = "email_exists"
            else:
                #OTP TO BE SENT VIA TWILIO (CODE PENDING)
                otp = str(random.randint(100000, 999999))
                response = f"otp|{otp}"
                print(f"OTP for {phone} and {email} is {otp}")
        except BaseException as msg:
            response = "otp_failed"
            print(msg)
        finally:
            c.send(response.encode())

    elif request_type == "signup":
        fname = data[1]
        nemail= data[2]
        phone= data[3]
        gender= data[4]
        bday= data[5]
        password= data[6].encode()
        hashed_password = hashlib.sha256(password).hexdigest()  
        try:
            query = "INSERT INTO user_data(fullname, email, phone, gender, bday, password) VALUES(%s, %s, %s, %s, %s, %s)"
            values= (fname, nemail, phone, gender, bday, hashed_password)
            dbs_connection.insert(query,values)
            response = "signup_success"
        except BaseException as error:
            print("Error: ", error)
            response = "signup_fail"
        finally:
            c.send(response.encode())

    elif request_type == "login":
        email = data[1]
        password = data[2].encode()
        hashed_password = hashlib.sha256(password).hexdigest()
        try:
            query = "SELECT fullname, email, password FROM user_data WHERE email = %s"
            result = dbs_connection.search(query, (email,))
            print(result)
            # f_name  = ""
            # f_email = ""
            # f_password = ""
            # for values in result:
            #     f_name_list = values[0]
            #     f_email_list = values[1]
            #     f_password_list = values[2]
            #     f_name = f_name_list
            #     f_email = f_email_list
            #     f_password = f_password_list
            if not result:
                response = "no_account"
            else:
                usr_name, usr_email, usr_password = result[0]
                print(result[0])
                if usr_password != hashed_password:
                    response = "incorrect_password"
                else:
                    response = f"login_success:{usr_name}:{usr_email}"
            # else:
            #     response = f"login_success:{f_name}:{f_email}"
        except BaseException as error:
            print("Error: ", error)
            response = "login_fail"
        finally:
            c.send(response.encode())

    elif request_type == "forgot_password":
        email = data[1]
        phone = data[2]
        try:
            query = "SELECT email,phone FROM user_data WHERE email = %s AND phone = %s"
            result = dbs_connection.search(query, (email,phone))
            print(result)
            if result == []:
                response = "no_account"
            else:
                #OTP TO BE SENT VIA TWILIO (CODE PENDING)
                otp = str(random.randint(100000, 999999))
                response = f"valid_account|{otp}"
                print(f"OTP for {phone} and {email} is {otp}")
        except BaseException as msg:
            response = "check_failed"
            print(msg)
        finally:
            c.send(response.encode())

    elif request_type == "change_password":
        email = data[1]
        phone = data[2]
        password = data[3].encode()
        hashed_password = hashlib.sha256(password).hexdigest()
        try:
            query = "UPDATE user_data SET password=%s WHERE email=%s AND phone=%s"
            values = (hashed_password, email, phone)
            dbs_connection.update(query,values)
            response = "password_changed"
        except:
            response = "password_change_failed"
        finally:
            c.send(response.encode())

    elif request_type == "message":
        time = data[1]
        sender = data[2]
        receiver = data[3]
        subject = data[4]
        message = data[5]

        try:
            query = "SELECT * FROM user_data WHERE email = %s"
            result = dbs_connection.search(query, (receiver,))
            if result == []:
                response = "no_receiver"
            else:
                try:
                    query = "INSERT INTO messages(time, sender, receiver, subject, message) VALUES(%s, %s, %s, %s, %s)"
                    values= (time, sender, receiver, subject, message)
                    dbs_connection.insert(query,values)
                    response = "message_sent"
                except BaseException as error:
                    print("Error: ", error)
                    response = "message_not_sent"
        finally:
            c.send(response.encode())

    elif request_type == "view_inbox":
        receiver = data[1]
        try:
            query = "SELECT *FROM messages WHERE receiver = %s"
            result = dbs_connection.search(query, (receiver,))
            if result == []:
                response = "empty_inbox"
            else:
                response = f"inbox|{result}"
        except BaseException as msg:
                response= "error"
                print(msg)
        finally:
            # print(response)
            c.send(response.encode())
    c.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '169.254.83.107'
    port = 1234
    server_socket.bind((host, port))
    server_socket.listen(5)
    print("Server Started...")

    while True:
        c, addr = server_socket.accept() 
        print ('Got connection from', addr )

        # Create a new thread to handle the connection
        t = threading.Thread(target=handle_connection, args=(c, addr))
        t.start()

if __name__ == '__main__':
    main()
