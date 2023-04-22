
from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
import forgotpassword
import re
import socket

#Creates a class where the login form is displayed
class Signin:
    activeusr_name = None
    activeusr_email = None
    def __init__(self,window):
        self.window = window
        self.window.geometry("1906x952+5+9")
        self.window.title("Sign in")
        self.window.resizable(False, False)
        
        self.background_img=ImageTk.PhotoImage \
            (file="images\\signinframe.png")
        self.background_image_panel = Label(self.window, image=self.background_img)
        self.background_image_panel.pack(fill='both', expand='yes')

        self.bmail_logo = ImageTk.PhotoImage \
            (file="images\\bmail.png")
        self.bmail_logo_panel = Label(self.window, image=self.bmail_logo, relief=FLAT, background="white", borderwidth=0)
        self.bmail_logo_panel.place(x=796, y=94)
        
        self.heading = Label(self.window, text="Sign in", font=("Inter", 20, "bold"), bg="white", fg='#000000')
        self.heading.place(x=881, y=257)
   
        ########## ON PRESSING X BUTTON TO CLOSE #############
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.email_label = Label(self.window, text="Email or phone", bg="white", fg="#000000", font=("Inter", 11, "bold"))
        self.email_label.place(x=753, y=336)
        self.email_entry = Entry(self.window, highlightthickness=0, relief=FLAT, bg="#EDEDED", fg="#000000",font=("Inter", 11, "bold"))
        self.email_entry.place(x=756, y=367, width=350, height=50)
        
        self.password_label = Label(self.window, text="Password ", bg="white", fg="#000000",font=("Inter", 11, "bold"))
        self.password_label.place(x=753, y=442)
        self.password_entry = Entry(self.window, highlightthickness=0, relief=FLAT, bg="#EDEDED", fg="#000000",font=("Inter", 11, "bold"), show="*")
        self.password_entry.place(x=756, y=473, width=350, height=50)
        
        # self.forgotpass_label = Label(self.window, text="Forgot password?", bg="white", fg="#000000", font=("Inter", 10, "bold"))
        # self.forgotpass_label.place(x=985, y=547)  

        self.forgot_label = Label(self.window, text="forgot ", bg="white", fg="#000000",
                                  font=("Inter", 11, "bold"))
        self.forgot_label.place(x=954, y=547)

        self.forgot_button = Button(self.window, text="password?",
                                    font=("Inter", 11, "bold"), fg="#FF0000", relief=FLAT,
                                    activebackground="white"
                                    , borderwidth=0, background="white", cursor="hand2", command=self.click_forgot)
        self.forgot_button.place(x=1009, y=543)

        self.signin_img = ImageTk.PhotoImage \
            (file="images\\signin.png")
        self.signin_button = Button(self.window, image=self.signin_img, relief=FLAT, activebackground="white"
                                   , borderwidth=0, background="white", cursor="hand2")#, command=self.validation)
        self.signin_button.place(x=860, y=611)
        
        self.signup_label1 = Label(self.window, text="Don't have ", bg="white", fg="#000000", font=("Inter", 11, "bold"))
        self.signup_label1.place(x=843, y=711)
        self.signup_label2 = Label(self.window, text="an account?", bg="white", fg="#FF0000", font=("Inter", 11, "bold"))
        self.signup_label2.place(x=941, y=711)


        self.signup_img = ImageTk.PhotoImage \
            (file="images\\signup.png")
        self.signup_button = Button(self.window, image=self.signup_img, relief=FLAT, activebackground="white"
                                   , borderwidth=0, background="white", cursor="hand2")#, command=self.click_signup)
        self.signup_button.place(x=860, y=747)


    def validation(self):
        try:
            if self.email_entry.get() == "":
                messagebox.showerror("Error", "Please enter email id")
            elif self.password_entry.get()=="":
                messagebox.showerror("Error", "Please enter password")
            elif self.is_valid_email() is False:
                messagebox.showerror("Error", "Invalid email format")
            else:
                self.login()

        except BaseException as msg:
            messagebox.showerror("Empty Field","Enter all the fields")
            print(msg)

    def login(self):
        try:
            c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host = socket.gethostname()
            #host= "192.168.1.8"	
            port = 1234			
            c.connect((host,port))
            email= self.email_entry.get()
            password= self.password_entry.get()
            c.send(f"login|{email}|{password}".encode())
            response = c.recv(1024).decode()
            if response == "Incorrect email":
                messagebox.showerror("Error", "Invalid Email id")
            elif response == "Incorrect password":
                messagebox.showerror("Error", "Incorrect password")
            elif response.startswith("Login_Success:"):
                data = response.split(":")
                Signin.activeusr_name = data[1]
                Signin.activeusr_email = data[2]
                self.login_success()

        except BaseException as msg:
            messagebox.showerror("Connection Failure","Failed to establish connection with server.")
            print(msg)

    def is_valid_email(self):
        pattern = r"^[a-z][a-z0-9]*@login\.com$"
        if re.match(pattern, self.email_entry.get()):
            return True
        return False
    
    def click_forgot(self):
        win= Toplevel()
        ForgotPassword(win)
        self.window.withdraw()
        win.deiconify()
        
        
    def on_closing(self):
        self.window.deiconify()
        ask = messagebox.askyesnocancel("Confirm exit", "Do you want to exit?")
        if ask is True:
            quit()


class ForgotPassword:
    def __init__(self,window):
        self.window = window
        self.window.geometry("1906x952+5+9")
        self.window.title("Forgot password")
        self.window.resizable(False, False)
        
        self.background_img=ImageTk.PhotoImage \
            (file="images\\forgotpasswordframe.png")
        self.background_image_panel = Label(self.window, image=self.background_img)
        self.background_image_panel.pack(fill='both', expand='yes')

        self.bmail_logo = ImageTk.PhotoImage \
            (file="images\\bmail.png")
        self.bmail_logo_panel = Label(self.window, image=self.bmail_logo, relief=FLAT, background="white", borderwidth=0)
        self.bmail_logo_panel.place(x=796, y=94)
        
        self.heading1 = Label(self.window, text="Forgot ", font=("Inter", 20, "bold"), bg="white", fg='#000000')
        self.heading1.place(x=808, y=257)
        self.heading2 = Label(self.window, text="password?", font=("Inter", 20, "bold"), bg="white", fg='#FF0000')
        self.heading2.place(x=921, y=257)
   
        ########## ON PRESSING X BUTTON TO CLOSE #############
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.email_label = Label(self.window, text="Email", bg="white", fg="#000000", font=("Inter", 11, "bold"))
        self.email_label.place(x=753, y=336)
        self.email_entry = Entry(self.window, highlightthickness=0, relief=FLAT, bg="#EDEDED", fg="#000000",font=("Inter", 11, "bold"))
        self.email_entry.place(x=756, y=367, width=350, height=50)
        
        self.phone_label = Label(self.window, text="Phone number", bg="white", fg="#000000",font=("Inter", 11, "bold"))
        self.phone_label.place(x=753, y=442)
        self.phone_entry = Entry(self.window, highlightthickness=0, relief=FLAT, bg="#EDEDED", fg="#000000",font=("Inter", 11, "bold"))
        self.phone_entry.place(x=756, y=473, width=350, height=50)

        self.otp_label = Label(self.window, text="OTP", bg="white", fg="#000000",font=("Inter", 11, "bold"))
        self.otp_label.place(x=753, y=546)
        self.otp_entry = Entry(self.window, highlightthickness=0, state=DISABLED ,disabledbackground="#808080",relief=FLAT, bg="#EDEDED", fg="#000000",font=("Inter", 11, "bold"))
        self.otp_entry.place(x=756, y=578, width=350, height=50)

        self.sendotp_img = ImageTk.PhotoImage \
            (file="images\\sendotp.png")
        self.submitotp_img = ImageTk.PhotoImage \
            (file="images\\submit.png")
        
        self.sendotp_button = Button(self.window, image=self.sendotp_img, relief=FLAT, activebackground="white"
                                   , borderwidth=0, background="white", cursor="hand2")#, command=self.click_sendotp)
        self.sendotp_button.place(x=860, y=663)
        # self.sendotp_button.is_clicked = False

        self.signin_label1 = Label(self.window, text="Go back to ", bg="white", fg="#000000", font=("Inter", 11, "bold"))
        self.signin_label1.place(x=853, y=741)
        self.signin_label2 = Label(self.window, text="sign in?", bg="white", fg="#FF0000", font=("Inter", 11, "bold"))
        self.signin_label2.place(x=951, y=741)

        self.signin_img = ImageTk.PhotoImage \
            (file="images\\signin.png")
        self.signin_button = Button(self.window, image=self.signin_img, relief=FLAT, activebackground="white"
                                   , borderwidth=0, background="white", cursor="hand2")#, command=self.click_signin)
        self.signin_button.place(x=860, y=772)

    def on_closing(self):
        self.window.deiconify()
        ask = messagebox.askyesnocancel("Confirm exit", "Do you want to exit?")
        if ask is True:
            quit()



def win():
    window = Tk()
    Signin(window)
    window.mainloop()


if __name__ == '__main__':
    win()