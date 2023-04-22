
from tkinter import *
from PIL import ImageTk
from tkinter.ttk import Combobox
from tkinter import messagebox
import re
import signin
import socket
from tkinter import ttk
class Signup:
    def __init__(self, window):
        self.window = window
        self.window.geometry("1906x952+5+9")
        self.window.title("Sign up")
        self.window.resizable(False, False)
        self.background_img=ImageTk.PhotoImage \
            (file="images\\signupframe.png")
        self.image_panel = Label(self.window, image=self.background_img)
        self.image_panel.pack(fill='both', expand='yes')
        

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
        
            
    def click_signin(self):
        win = Toplevel()
        self.window.withdraw()
        signin.Signin(win)
        win.deiconify()
        
    def click_submit(self):
        try:
            if self.fullname_entry.get() == "":
                messagebox.showerror("Error", "Enter full name")
            elif self.month_combobox.get() == "Month" or self.day_combobox.get() == "Day" or self.year_combobox.get() == "Year":
                messagebox.showerror("Error", "Select date of birth")
            elif self.gender_combobox.get() == "Select":
                messagebox.showerror("Error", "Select gender.")
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
                try:  
                    self.selected_month = self.month_combobox.get()
                    self.selected_day = self.day_combobox.get()
                    self.selected_year = self.year_combobox.get()

                    # Convert the month value to a month number
                    self.month_number = int({"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
                        "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}[self.selected_month])

                    # Construct the date value in the format 'YYYY-MM-DD'
                    self.selected_birthdate = f"{self.selected_year}-{self.month_number:02d}-{int(self.selected_day):02d}"

                    ask = messagebox.askyesnocancel("Confirm Signup", "Proceed to signup?")
                    if ask is True:
                        pass
                        # self.signup()
                except BaseException as msg:
                    print(msg)

        except BaseException as msg:
            messagebox.showerror("Error", "Fill all the details")

          
    def signup(self):
        try:
            c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host = socket.gethostname()
            #host= "192.168.1.8"	
            port = 1234			
            c.connect((host,port))
            fname = self.fullname_entry.get()
            nemail= self.newemail_entry.get()
            gender= self.gender_combobox.get()
            bday= self.selected_birthdate
            password= self.newpassword_entry.get()
            c.send(f"signup|{fname}|{nemail}|{gender}|{bday}|{password}".encode())
            response = c.recv(1024).decode()
            if response == "Email already exists":
                messagebox.showerror("Error", "Email id already exists. Choose different email address.")
            elif response == "signup_success":
                messagebox.showinfo("Success", "Account has been created. Please proceed to login.")
                self.click_gobacktologin()
            elif response == "signup_fail":
                messagebox.showerror("Failed", "Signup Failed")
        except:
            messagebox.showerror("Connection Failure","Failed to establish connection with server.")

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

    def on_closing(self):
        self.window.deiconify()
        ask = messagebox.askyesnocancel("Confirm exit", "Do you want to exit?")
        if ask is True:
            quit()
        
                
def win():
    window = Tk()
    Signup(window)
    window.mainloop()

if __name__ == '__main__':
    win()