from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
from tkinter.ttk import Combobox
import re
import connection
import main

#Creates a class where the login form is displayed
class Signin:
    activeusr_id = None
    activeusr_name = None
    activeusr_email = None
    def __init__(self,window, socket_connection):
        self.window = window
        self.window.geometry("1906x952+5+9")
        self.window.title("Sign in")
        self.window.resizable(False, False)
        self.socket_connection = socket_connection

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
        
        self.email_label = Label(self.window, text="Email", bg="white", fg="#000000", font=("Inter", 11, "bold"))
        self.email_label.place(x=753, y=336)
        self.email_entry = Entry(self.window, highlightthickness=0, relief=FLAT, bg="#EDEDED", fg="#000000",font=("Inter", 11, "bold"))
        self.email_entry.place(x=756, y=367, width=350, height=50)
        
        self.password_label = Label(self.window, text="Password ", bg="white", fg="#000000",font=("Inter", 11, "bold"))
        self.password_label.place(x=753, y=442)
        self.password_entry = Entry(self.window, highlightthickness=0, relief=FLAT, bg="#EDEDED", fg="#000000",font=("Inter", 11, "bold"), show="*")
        self.password_entry.place(x=756, y=473, width=350, height=50)

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
                                   , borderwidth=0, background="white", cursor="hand2", command=self.click_signin)
        self.signin_button.place(x=860, y=611)
        
        self.signup_label1 = Label(self.window, text="Don't have ", bg="white", fg="#000000", font=("Inter", 11, "bold"))
        self.signup_label1.place(x=843, y=711)
        self.signup_label2 = Label(self.window, text="an account?", bg="white", fg="#FF0000", font=("Inter", 11, "bold"))
        self.signup_label2.place(x=941, y=711)

        self.signup_img = ImageTk.PhotoImage \
            (file="images\\signup.png")
        self.signup_button = Button(self.window, image=self.signup_img, relief=FLAT, activebackground="white"
                                   , borderwidth=0, background="white", cursor="hand2", command=self.click_signup)
        self.signup_button.place(x=860, y=747)


    def click_signin(self):
        try:
            if self.email_entry.get() == "":
                messagebox.showerror("Empty field", "Enter Email")
            elif self.password_entry.get()=="":
                messagebox.showerror("Empty field", "Enter Password")
            else:
                self.signin()

        except BaseException as msg:
            messagebox.showerror("Empty Field","Enter all the fields")
            print(msg)

    def signin(self):
        try:
            request = {
                'type': 'login',
                'email': self.email_entry.get() ,
                'password': self.password_entry.get()
            }
            self.socket_connection.send(request)
            response = self.socket_connection.receive()
            if response['type'] == "no_account":
                messagebox.showerror("Account error", "Account doesnot exists on our system")
            elif response['type'] == "incorrect_password":
                messagebox.showerror("Password error", "Incorrect password")
            elif response['type'] == "login_success":
                Signin.activeusr_id = response['active_id']
                Signin.activeusr_name = response['active_user']
                Signin.activeusr_email = response['active_email']
                self.signin_success()
            elif response['type'] == 'login_fail':
                messagebox.showerror("Failure","Login failed")
        except ConnectionRefusedError as msg:
            messagebox.showerror("Connection Failure","Failed to establish connection with server.")
            print(msg)
    
    def click_forgot(self):
        win= Toplevel()
        self.window.withdraw()
        ForgotPassword(win, self.socket_connection)
        win.deiconify()
 
    def click_signup(self):
        win = Toplevel()
        self.window.withdraw()
        Signup(win, self.socket_connection)
        win.deiconify()

    def on_closing(self):
        self.window.deiconify()
        ask = messagebox.askyesnocancel("Confirm exit", "Do you want to exit?")
        if ask is True:
            quit()

    def signin_success(self):
        id = Signin.activeusr_id
        email= Signin.activeusr_email
        name= Signin.activeusr_name
        win = Toplevel()
        main.Home(win, id,email, name, self.socket_connection)
        self.window.withdraw()
        win.deiconify()

class ForgotPassword:
    email = None
    phone = None
    otp = None
    def __init__(self,window,socket_connection):
        self.window = window
        self.window.geometry("1906x952+5+9")
        self.window.title("Forgot password")
        self.window.resizable(False, False)

        self.socket_connection = socket_connection

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
                                   , borderwidth=0, background="white", cursor="hand2", command=self.click_sendotp)
        self.sendotp_button.place(x=860, y=663)

        self.signin_label1 = Label(self.window, text="Go back to ", bg="white", fg="#000000", font=("Inter", 11, "bold"))
        self.signin_label1.place(x=853, y=741)
        self.signin_label2 = Label(self.window, text="sign in?", bg="white", fg="#FF0000", font=("Inter", 11, "bold"))
        self.signin_label2.place(x=951, y=741)

        self.signin_img = ImageTk.PhotoImage \
            (file="images\\signin.png")
        self.signin_button = Button(self.window, image=self.signin_img, relief=FLAT, activebackground="white"
                                   , borderwidth=0, background="white", cursor="hand2", command=self.click_signin)
        self.signin_button.place(x=860, y=772)


    def click_sendotp(self):
            if self.email_entry.get() == "":
                messagebox.showerror("Empty field","Enter email")
            elif self.phone_entry.get() == "":
                messagebox.showerror("Empty field","Enter phonenumber")
            else:
                try:
                    request = {
                        'type': 'forgot_password',
                        'email': self.email_entry.get() ,
                        'phone': f"+977{self.phone_entry.get()}"
                    }
                    self.socket_connection.send(request)
                    response = self.socket_connection.receive()
                    if response['type'] == "no_account":
                        messagebox.showerror("Incorrect id or phonenumber","Credentials doesn't matched with our system")
                    elif response['type'] == "error":
                        messagebox.showerror("Server issue", "Server is disconnected")
                    elif response['type'] == "valid_account":
                        otp = response['otp']
                        ForgotPassword.email = self.email_entry.get()
                        ForgotPassword.phone = f"+977{self.phone_entry.get()}"
                        ForgotPassword.otp = otp
                        self.otp_entry.configure(state=NORMAL)
                        self.email_entry.configure(state=DISABLED)
                        self.phone_entry.configure(state=DISABLED)
                        self.sendotp_button.configure(image=self.submitotp_img, command=self.click_submit)
                        messagebox.showinfo("OTP sent","Otp has been sent to verified phone number")
                        
                except ConnectionRefusedError as msg:
                    messagebox.showerror("Connection Failure","Failed to establish connection with server.")
                    print(msg)


    def click_submit(self):
        if self.otp_entry.get() == "":
            messagebox.askokcancel("Empty field","Enter otp")
        elif self.valid_otp() is False:
            messagebox.askokcancel("OTP","OTP should be six digits only")
        elif self.otp_entry.get() != ForgotPassword.otp:
            messagebox.showerror("Otp","Incorrect otp")
        elif self.otp_entry.get() == ForgotPassword.otp:
            self.change_password()

    def valid_otp(self):
        pattern = r"^[0-9]{6}$"
        if re.match(pattern, self.otp_entry.get()):
            return True
        return False

    def change_password(self):
        email = ForgotPassword.email
        phone = ForgotPassword.phone
        win = Toplevel()
        ChangePassword(win, self.socket_connection, email, phone)
        self.window.withdraw()
        win.deiconify()

    def click_signin(self):
        win = Toplevel()
        self.window.withdraw()
        Signin(win, self.socket_connection)
        win.deiconify()

    def on_closing(self):
        self.window.deiconify()
        ask = messagebox.askyesnocancel("Confirm exit", "Do you want to exit?")
        if ask is True:
            quit()


class ChangePassword:
    def __init__(self,window,socket_connection, email, phone):
        self.window = window
        self.window.geometry("1906x952+5+9")
        self.window.title("Change Password")
        self.window.resizable(False, False)

        self.socket_connection = socket_connection
        self.email = email
        self.phone = phone
        
        self.background_img=ImageTk.PhotoImage \
            (file="images\\signinframe.png")
        self.background_image_panel = Label(self.window, image=self.background_img)
        self.background_image_panel.pack(fill='both', expand='yes')

        self.bmail_logo = ImageTk.PhotoImage \
            (file="images\\bmail.png")
        self.bmail_logo_panel = Label(self.window, image=self.bmail_logo, relief=FLAT, background="white", borderwidth=0)
        self.bmail_logo_panel.place(x=796, y=94)
        
        self.heading = Label(self.window, text="Change Password", font=("Inter", 20, "bold"), bg="white", fg='#000000')
        self.heading.place(x=802, y=257)
   
        ########## ON PRESSING X BUTTON TO CLOSE #############
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.newpassword_label = Label(self.window, text="New password", bg="white", fg="#000000", font=("Inter", 11, "bold"))
        self.newpassword_label.place(x=753, y=336)
        self.newpassword_entry = Entry(self.window, highlightthickness=0, relief=FLAT, bg="#EDEDED", fg="#000000",font=("Inter", 11, "bold"), show="*")
        self.newpassword_entry.place(x=756, y=367, width=350, height=50)
        
        self.confirmpassword_label = Label(self.window, text="Confirm Password", bg="white", fg="#000000",font=("Inter", 11, "bold"))
        self.confirmpassword_label.place(x=753, y=442)
        self.confirmpassword_entry = Entry(self.window, highlightthickness=0, relief=FLAT, bg="#EDEDED", fg="#000000",font=("Inter", 11, "bold"), show="*")
        self.confirmpassword_entry.place(x=756, y=473, width=350, height=50)


        self.submit_img = ImageTk.PhotoImage \
            (file="images\\submit.png")
        self.submit_button = Button(self.window, image=self.submit_img, relief=FLAT, activebackground="white"
                                   , borderwidth=0, background="white", cursor="hand2", command=self.click_submit)
        self.submit_button.place(x=860, y=611)
        
        self.signup_label1 = Label(self.window, text="Go back to ", bg="white", fg="#000000", font=("Inter", 11, "bold"))
        self.signup_label1.place(x=843, y=711)
        self.signup_label2 = Label(self.window, text="sign in?", bg="white", fg="#FF0000", font=("Inter", 11, "bold"))
        self.signup_label2.place(x=941, y=711)


        self.signin_img = ImageTk.PhotoImage \
            (file="images\\signin.png")
        self.signin_button = Button(self.window, image=self.signin_img, relief=FLAT, activebackground="white"
                                   , borderwidth=0, background="white", cursor="hand2", command=self.click_signin)
        self.signin_button.place(x=860, y=747)

    def click_submit(self):
        if self.newpassword_entry.get()=="":
            messagebox.showerror("Empty field","Enter new password")
        elif  self.confirmpassword_entry.get()=="":
            messagebox.showerror("Empty field","Enter confirm password field")
        elif self.newpassword_entry.get() != self.confirmpassword_entry.get():
            messagebox.showerror("Mismatch","Password mismatch")
        else:
            try:
                request = {
                    'type': 'change_password',
                    'email': self.email ,
                    'phone': self.phone,
                    'password': self.newpassword_entry.get()
                }
                self.socket_connection.send(request)
                response = self.socket_connection.receive()
                if response['type'] == "password_changed":
                    self.newpassword_entry.delete(0, END)
                    self.confirmpassword_entry.delete(0, END)
                    messagebox.showinfo("Password changed","Password has been changed")
                    self.click_signin()
                elif response['type'] == "password_change_failed":
                    messagebox.showerror("Server issue","Password change failed")
            except ConnectionRefusedError as msg:
                messagebox.showerror("Connection Failure","Failed to establish connection with server.")
                print(msg)

    def click_signin(self):
        win = Toplevel()
        self.window.withdraw()
        Signin(win, self.socket_connection)
        win.deiconify()

    def on_closing(self):
        self.window.deiconify()
        ask = messagebox.askyesnocancel("Confirm exit", "Do you want to exit?")
        if ask is True:
            quit()

class Signup:
    fname = None
    nemail = None
    phone = None
    gender = None
    bday = None
    password = None
    otp = None
    def __init__(self, window,socket_connection):
        self.window = window
        self.window.geometry("1906x952+5+9")
        self.window.title("Sign up")
        self.window.resizable(False, False)

        self.socket_connection = socket_connection

        self.background_img=ImageTk.PhotoImage \
            (file="images\\signupframe.png")
        self.image_panel = Label(self.window, image=self.background_img)
        self.image_panel.pack(fill='both', expand='yes')
        
        self.socket_connection = socket_connection

        self.bmail_logo = ImageTk.PhotoImage \
            (file="images\\bmail.png")
        self.bmail_logo_panel = Label(self.window, image=self.bmail_logo, relief=FLAT, background="white", borderwidth=0)
        self.bmail_logo_panel.place(x=796, y=94)

        self.heading = Label(self.window, text="Sign up", font=("Inter", 20, "bold"), bg="white", fg='#000000')
        self.heading.place(x=876, y=193)
        
        ########## ON PRESSING X BUTTON TO CLOSE #############
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing) 

        self.fullname_label = Label(self.window, text="Full name", bg="white", fg="Black",font=("Inter", 9, "bold"))
        self.fullname_label.place(x=752, y=246)
        self.fullname_entry = Entry(self.window, highlightthickness=0, relief=FLAT, bg="#EDEDED", fg="#000000",font=("Inter", 10, "bold"))
        self.fullname_entry.place(x=756, y=275, width=350, height=40)


        self.bday_label = Label(self.window, text="Date of birth", bg="white", fg="#000000",font=("Inter", 9, "bold"))
        self.bday_label.place(x=752, y=323)
        self.month_var = StringVar(value="Month")
        self.month_combobox = Combobox(self.window, values=["January", "February", "March", "April", "May", "June",
         "July", "August", "September", "October", "November", "December"], state="readonly", textvariable=self.month_var)
        self.month_combobox.place(x=755, y=359, width=113)
        self.month_combobox.configure(font=("Inter", 10, "bold"))
        self.day_var = StringVar(value="Day")
        self.day_combobox = Combobox(self.window, values=list(range(1,32)), state="readonly", textvariable=self.day_var)
        self.day_combobox.place(x=869, y=359, width=57)
        self.day_combobox.configure(font=("Inter", 10, "bold"))
        self.year_var = StringVar(value="Year")
        self.year_combobox = Combobox(self.window, values=list(range(2023,1923,-1)), state="readonly", textvariable=self.year_var)
        self.year_combobox.place(x=928, y=359, width=70)
        self.year_combobox.configure(font=("Inter", 10, "bold"))

        self.gender_label = Label(self.window, text="Sex", bg="white", fg="#000000",font=("Inter", 9, "bold"))
        self.gender_label.place(x=1000, y=323)
        self.gender_var = StringVar(value="Select")
        self.gender_combobox = Combobox(self.window, values=["Male", "Female"], state="readonly", textvariable=self.gender_var)
        self.gender_combobox.place(x=1013, y=359, width=95)
        self.gender_combobox.configure(font=("Inter", 10, "bold"))

        self.phonenumber_label = Label(self.window, text="Phone number", bg="white", fg="#000000",font=("Inter", 9, "bold"))
        self.phonenumber_label.place(x=752, y=400)
        self.phonenumber_entry = Entry(self.window, highlightthickness=0, relief=FLAT, bg="#EDEDED", fg="#000000",font=("Inter", 10, "bold"))
        self.phonenumber_entry.place(x=756, y=429, width=350, height=40)

        self.newemail_label = Label(self.window, text="Email", bg="white", fg="#000000",font=("Inter", 9, "bold"))
        self.newemail_label.place(x=752, y=477)
        self.newemail_entry = Entry(self.window, highlightthickness=0, relief=FLAT, bg="#EDEDED", fg="#000000",font=("Inter", 10, "bold"))
        self.newemail_entry.place(x=756, y=506, width=350, height=40)
        
        self.newpassword_label = Label(self.window, text="Password", bg="white", fg="#000000",font=("Inter", 9, "bold"))
        self.newpassword_label.place(x=752, y=554)
        self.newpassword_entry = Entry(self.window, highlightthickness=0, relief=FLAT, bg="#EDEDED", fg="#000000",font=("Inter", 10, "bold"), show="*")
        self.newpassword_entry.place(x=756, y=583, width=350, height=40)
        
        self.confirm_newpassword_label = Label(self.window, text="Confirm password", bg="white", fg="#000000",font=("Inter", 9, "bold"))
        self.confirm_newpassword_label.place(x=752, y=631)
        self.confirm_newpassword_entry = Entry(self.window, highlightthickness=0, relief=FLAT, bg="#EDEDED", fg="#000000",font=("Inter", 10, "bold"), show="*")
        self.confirm_newpassword_entry.place(x=756, y=660, width=350, height=40)
        
        self.submit_img = ImageTk.PhotoImage \
            (file="images\\submit.png")
        self.submit_button = Button(self.window, image=self.submit_img, relief=FLAT, activebackground="white"
                                   , borderwidth=0, background="white", cursor="hand2", command=self.click_submit)
        self.submit_button.place(x=860, y=737)

        self.signin1_label = Label(self.window, text="Sign in ", bg="white", fg="#FF0000",font=("Inter", 11, "bold"))
        self.signin1_label.place(x=865, y=814)
        self.signin2_label = Label(self.window, text="instead?", bg="white", fg="#000000",font=("Inter", 11, "bold"))
        self.signin2_label.place(x=929, y=814)

        self.signin_img = ImageTk.PhotoImage \
            (file="images\\signin.png")
        self.signin_button = Button(self.window, image=self.signin_img, relief=FLAT, activebackground="white"
                                   , borderwidth=0, background="white", cursor="hand2", command=self.click_signin)
        self.signin_button.place(x=860, y=844)
        
    def click_submit(self):
        try:
            if self.fullname_entry.get() == "":
                messagebox.showerror("Error", "Enter full name")
            elif self.month_combobox.get() == "Month" or self.day_combobox.get() == "Day" or self.year_combobox.get() == "Year":
                messagebox.showerror("Error", "Select date of birth")
            elif self.gender_combobox.get() == "Select":
                messagebox.showerror("Error", "Select gender.")
            elif self.phonenumber_entry.get() == "":
                messagebox.showerror("Error","Enter phone number")
            elif self.newemail_entry.get() == "":
                messagebox.showerror("Error", "Enter email")
            elif self.newpassword_entry.get() == "":
                messagebox.showerror("Error", "Enter password")
            elif self.confirm_newpassword_entry.get() == "":
                messagebox.showerror("Error", "Confirm password")
            elif self.newpassword_entry.get() != self.confirm_newpassword_entry.get():
                messagebox.showerror("Error", "Password mismatch")
            elif self.is_valid_phonenumber() is False:
                messagebox.showerror("Error","Enter ten digit phone number")
            elif self.is_valid_email() is False:
                messagebox.showerror("Error", "Invalid email format \n Try example123@bmail.com as format")
            else:
                self.signup()

        except BaseException as msg:
            messagebox.showerror("Error", "Fill all the details")

    def signup(self):
        Signup.fname = self.fullname_entry.get()
        Signup.nemail= self.newemail_entry.get()
        Signup.phone= f"+977{self.phonenumber_entry.get()}"
        Signup.gender= self.gender_combobox.get()

        #Change birthdate format
        self.selected_month = self.month_combobox.get()
        self.selected_day = self.day_combobox.get()
        self.selected_year = self.year_combobox.get()
        self.month_number = int({"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
            "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}[self.selected_month])
        self.selected_birthdate = f"{self.selected_year}-{self.month_number:02d}-{int(self.selected_day):02d}"

        Signup.bday= self.selected_birthdate
        Signup.password= self.newpassword_entry.get()

        try:
            request = {
                'type': 'verify_signup',
                'email': self.newemail_entry.get() ,
                'phone': f"+977{self.phonenumber_entry.get()}"
            }
            self.socket_connection.send(request)
            response = self.socket_connection.receive()
            if response['type'] == "email_exists":
                messagebox.showerror("Email exists","Email already in use. Choose different email address")
            elif response['type'] == "otp_failed":
                messagebox.showerror("Failed","Failed to send otp")
            elif response['type'] == "otp":
                otp = response['otp']
                Signup.otp = otp
                self.verify_phone()

        except ConnectionRefusedError as msg:
            messagebox.showerror("Connection Failure","Failed to establish connection with server.")
            print(msg)

        except BaseException as msg:
            print(msg)

    def verify_phone(self):
        fname = Signup.fname
        nemail = Signup.nemail
        phone = Signup.phone
        gender = Signup.gender
        bday = Signup.bday
        password = Signup.password
        otp = Signup.otp
        win = Toplevel()
        self.window.withdraw()
        VerifyOTP(win,self.socket_connection,fname,nemail,phone,gender,bday,password,otp)
        win.deiconify()

    def is_valid_email(self):
        pattern = r"^[a-z][a-z0-9]*@bmail\.com$"
        if re.match(pattern, self.newemail_entry.get()):
            return True
        return False
    
    def is_valid_phonenumber(self):
        pattern = r"^[0-9]{10}$"
        if re.match(pattern, self.phonenumber_entry.get()):
            return True
        return False
    
    def click_signin(self):
        win = Toplevel()
        self.window.withdraw()
        Signin(win, self.socket_connection)
        win.deiconify()

    def on_closing(self):
        self.window.deiconify()
        ask = messagebox.askyesnocancel("Confirm exit", "Do you want to exit?")
        if ask is True:
            quit()

class VerifyOTP:
    def __init__(self, window, socket_connection,fname,nemail,phone,gender,bday,password,otp):
        self.window = window
        self.window.geometry("1906x952+5+9")
        self.window.title("Verify")
        self.window.resizable(False, False)

        self.socket_connection = socket_connection

        self.fname= fname
        self.nemail= nemail
        self.phone= phone
        self.gender= gender
        self.bday= bday
        self.password= password
        self.otp= otp

        ########## ON PRESSING X BUTTON TO CLOSE #############
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing) 

        self.background_img=ImageTk.PhotoImage \
            (file="images\\verifyframe.png")
        self.image_panel = Label(self.window, image=self.background_img)
        self.image_panel.pack(fill='both', expand='yes')
        
        self.bmail_logo = ImageTk.PhotoImage \
            (file="images\\bmail.png")
        self.bmail_logo_panel = Label(self.window, image=self.bmail_logo, relief=FLAT, background="white", borderwidth=0)
        self.bmail_logo_panel.place(x=796, y=94)

        self.heading_label = Label(self.window, text="Verify your phone number", font=("Inter", 20, "bold"), bg="white", fg='#000000')
        self.heading_label.place(x=722, y=257)

        self.message_label1 = Label(self.window, text="Due to security concern, ", bg="white", fg="#000000", font=("Inter", 11, "bold"))
        self.message_label1.place(x=703, y=351)
        self.message_label2 = Label(self.window, text="Bmail ", bg="white", fg="#5356FB", font=("Inter", 11, "bold"))
        self.message_label2.place(x=922, y=351)
        self.message_label3 = Label(self.window, text="wants to make sure ", bg="white", fg="#000000", font=("Inter", 11, "bold"))
        self.message_label3.place(x=977, y=351)
        self.message_label4 = Label(self.window, text="it's really you. ", bg="white", fg="#000000", font=("Inter", 11, "bold"))
        self.message_label4.place(x=723, y=380)
        self.message_label5 = Label(self.window, text="Bmail ", bg="white", fg="#5356FB", font=("Inter", 11, "bold"))
        self.message_label5.place(x=850, y=380)
        self.message_label4 = Label(self.window, text="will send a text message", bg="white", fg="#000000", font=("Inter", 11, "bold"))
        self.message_label4.place(x=905, y=380)
        self.message_label4 = Label(self.window, text="with a 6-digit OTP to signup.", bg="white", fg="#000000", font=("Inter", 11, "bold"))
        self.message_label4.place(x=795, y=410)

        self.otp_label = Label(self.window, text="OTP", bg="white", fg="Black",font=("Inter", 11, "bold"))
        self.otp_label.place(x=752, y=464)
        self.otp_entry = Entry(self.window, highlightthickness=0, relief=FLAT, bg="#EDEDED", fg="#000000",font=("Inter", 11, "bold"))
        self.otp_entry.place(x=755, y=495, width=350, height=50)

        self.verify_img = ImageTk.PhotoImage \
            (file="images\\verify.png")
        self.verify_button = Button(self.window, image=self.verify_img, relief=FLAT, activebackground="white"
                                   , borderwidth=0, background="white", cursor="hand2", command=self.click_verify)
        self.verify_button.place(x=753, y=620)

        self.cancel_img = ImageTk.PhotoImage \
            (file="images\\cancel.png")
        self.cancel_button = Button(self.window, image=self.cancel_img, relief=FLAT, activebackground="white"
                                   , borderwidth=0, background="white", cursor="hand2", command=self.goto_signup)
        self.cancel_button.place(x=969, y=619)

    def click_verify(self):
        try:
            if self.valid_otp() is False:
                messagebox.askokcancel("OTP","OTP should be six digit numbers only")
            elif self.otp_entry.get() == self.otp:
                self.otp_entry.configure(state=DISABLED)
                self.verified()
            elif self.otp_entry.get() != self.otp:
                messagebox.showerror("OTP","Incorrect otp")
        except BaseException as msg:
            print(msg)

    def verified(self):
        try:
            request = {
                'type': 'signup',
                'name': self.fname ,
                'email': self.nemail,
                'phone':  self.phone,
                'gender': self.gender,
                'bday': self.bday,
                'password': self.password
            }
            self.socket_connection.send(request)
            response = self.socket_connection.receive()
            if response['type'] == "signup_success":
                messagebox.showinfo("Success", "Account has been created. Proceed to signin")
                self.goto_signin()
            elif response['type'] == "signup_fail":
                messagebox.showerror("Failed", "Account creation has failed. Try later")
                self.goto_signup()
        except ConnectionRefusedError as msg:
            messagebox.showerror("Connection Failure","Failed to establish connection with server.")
            print(msg)

    def valid_otp(self):
        pattern = r"^[0-9]{6}$"
        if re.match(pattern, self.otp_entry.get()):
            return True
        return False
    
    def goto_signup(self):
        win = Toplevel()
        self.window.withdraw()
        Signup(win, self.socket_connection)
        win.deiconify()

    def goto_signin(self):
        win = Toplevel()
        self.window.withdraw()
        Signin(win,self.socket_connection)
        win.deiconify()

    def on_closing(self):
        self.window.deiconify()
        ask = messagebox.askyesnocancel("Confirm exit", "Do you want to exit?")
        if ask is True:
            quit()


def win():
        window = Tk()
        socket_connection = connection.SocketConnection() 
        Signin(window, socket_connection)
        window.mainloop()

if __name__ == '__main__':
    win()