
from tkinter import *
from PIL import ImageTk
from tkinter.ttk import Combobox
from tkinter import messagebox
import re
import login
import socket

class Signup:
    def __init__(self, window):
    
        self.window = window
        self.window.geometry("1366x720+250+100")
        self.window.title("Signup Page")
        self.window.resizable(False, False)
        
        self.background_img=ImageTk.PhotoImage \
            (file="images\\signupbg1.png")
        self.image_panel = Label(self.window, image=self.background_img)
        self.image_panel.pack(fill='both', expand='yes')
        
        self.heading = Label(self.window, text="Sign up", font=("Times", 30,), bg="white", fg='red', relief=FLAT)
        self.heading.place(x=400, y=60, width=450)
        
        ########## ON PRESSING X BUTTON TO CLOSE #############
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing) 

        self.fullname_label = Label(self.window, text="Full name", bg="white", fg="Black",font=("yu gothic ui", 11, "bold"))
        self.fullname_label.place(x=420, y=137)
        self.fullname_entry = Entry(self.window, highlightthickness=0, relief=FLAT, bg="white", fg="#4f4e4d",font=("sans-serif", 11))
        self.fullname_entry.place(x=450, y=170, width=380)

        self.gender_label = Label(self.window, text="Gender", bg="white", fg="Black",font=("yu gothic ui", 11, "bold"))
        self.gender_label.place(x=420, y=210)
        self.gender_var = StringVar(value="Select")
        self.gender_combobox = Combobox(self.window, values=["Male", "Female"], state="readonly", textvariable=self.gender_var)
        self.gender_combobox.place(x=453, y=240, width=105)
        self.gender_combobox.config(font=("sans-serif", 11))

        self.bday_label = Label(self.window, text="Birth date", bg="white", fg="Black",font=("yu gothic ui", 11, "bold"))
        self.bday_label.place(x=420, y=282)
        self.month_var = StringVar(value="Month")
        self.month_combobox = Combobox(self.window, values=["January", "February", "March", "April", "May", "June",
         "July", "August", "September", "October", "November", "December"], state="readonly", textvariable=self.month_var)
        self.month_combobox.place(x=453, y=310, width=118)
        self.month_combobox.config(font=("sans-serif", 11))
        self.day_var = StringVar(value="Day")
        self.day_combobox = Combobox(self.window, values=list(range(1,32)), state="readonly", textvariable=self.day_var)
        self.day_combobox.place(x=577, y=310, width=70)
        self.day_combobox.config(font=("sans-serif", 11))
        self.year_var = StringVar(value="Year")
        self.year_combobox = Combobox(self.window, values=list(range(2023,1923,-1)), state="readonly", textvariable=self.year_var)
        self.year_combobox.place(x=654, y=310, width=90)
        self.year_combobox.config(font=("sans-serif", 11))

        self.newemail_label = Label(self.window, text="Create new email", bg="white", fg="Black",font=("yu gothic ui", 11, "bold"))
        self.newemail_label.place(x=420, y=353)
        self.newemail_entry = Entry(self.window, highlightthickness=0, relief=FLAT, bg="white", fg="#4f4e4d",font=("sans-serif", 11))
        self.newemail_entry.place(x=450, y=383, width=380)
        self.newemail_entry.insert(0, 'example@login.com')
        self.newemail_entry.bind('<FocusIn>',self.on_enter)
        self.newemail_entry.bind('<FocusOut>',self.on_leave)
        
        self.newpassword_label = Label(self.window, text="Create new password", bg="white", fg="Black",font=("yu gothic ui", 11, "bold"))
        self.newpassword_label.place(x=420, y=420)
        self.newpassword_entry = Entry(self.window, highlightthickness=0, relief=FLAT, bg="white", fg="#4f4e4d",font=("sans-serif", 11), show="*")
        self.newpassword_entry.place(x=450, y=454, width=380)
        
        self.confirm_newpassword_label = Label(self.window, text="Confirm password", bg="white", fg="Black",font=("yu gothic ui", 11, "bold"))
        self.confirm_newpassword_label.place(x=420, y=493)
        self.confirm_newpassword_entry = Entry(self.window, highlightthickness=0, relief=FLAT, bg="white", fg="#4f4e4d",font=("sans-serif", 11), show="*")
        self.confirm_newpassword_entry.place(x=450, y=527, width=380)
        
        self.goback_img = ImageTk.PhotoImage \
            (file="images\\goback.png")
        self.goback_button = Button(self.window, image=self.goback_img,
                                   font=("yu gothic ui", 13, "bold"), relief=FLAT, activebackground="white"
                                   , borderwidth=0, background="white", cursor="hand2", command=self.click_gobacktologin)
        self.goback_button.place(x=480, y=600)
        
        self.submit_img = ImageTk.PhotoImage \
            (file="images\\submitbutton.png")
        self.submit_button = Button(self.window, image=self.submit_img,
                                   font=("yu gothic ui", 13, "bold"), relief=FLAT, activebackground="white"
                                   , borderwidth=0, background="white", cursor="hand2", command=self.click_submit)
        self.submit_button.place(x=640, y=600)
        
    def on_enter(self, event):
        self.newemail_entry.delete(0, 'end')
        
    def on_leave(self, event):
        enter_em=self.newemail_entry.get()
        if enter_em == "":
            self.newemail_entry.insert(0, 'example@login.com')
            
    def click_gobacktologin(self):
        win = Toplevel()
        login.Login(win)
        self.window.withdraw()
        win.deiconify()
        
    def click_submit(self):
        try:
            if self.fullname_entry.get() == "":
                messagebox.showerror("Error", "Please enter your full name")
            elif self.gender_combobox.get() == "Select":
                messagebox.showerror("Error", "Select your gender.")
            elif self.month_combobox.get() == "Month" or self.day_combobox.get() == "Day" or self.year_combobox.get() == "Year":
                messagebox.showerror("Error", "Please enter your birth date")
            elif self.newemail_entry.get() == "" or self.newemail_entry.get() == "example@login.com":
                messagebox.showerror("Error", "Please enter new email")
            elif self.newpassword_entry.get() == "":
                messagebox.showerror("Error", "Please enter new password")
            elif self.confirm_newpassword_entry.get() == "":
                messagebox.showerror("Error", "Please confirm your password")
            elif self.newpassword_entry.get() != self.confirm_newpassword_entry.get():
                messagebox.showerror("Error", "Password mismatch")
            elif self.is_valid_email() is False:
                messagebox.showerror("Error", "Invalid email format")
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
                        self.signup()
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
        pattern = r"^[a-z][a-z0-9]*@login\.com$"
        if re.match(pattern, self.newemail_entry.get()):
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