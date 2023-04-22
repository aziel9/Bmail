from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
import signin
import changepassword
import re
import socket

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
                                   , borderwidth=0, background="white", cursor="hand2", command=self.click_sendotp)
        self.sendotp_button.place(x=860, y=663)
        # self.sendotp_button.is_clicked = False

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
            ask = messagebox.askyesno("Confirm", f"OTP will be sent to {self.phone_entry.get()} \n Confirm this phone number?")
            if ask is True:
                messagebox.showinfo("Sent", f"OTP has been sent to {self.phone_entry.get()}\n Please enter OTP to continue")
                self.otp_entry.configure(state=NORMAL)
                self.email_entry.configure(state=DISABLED)
                self.phone_entry.configure(state=DISABLED)
                self.sendotp_button.configure(image=self.submitotp_img, command=self.click_submit)

    def click_submit(self):
        messagebox.showinfo("Success", "OTP verified. \n Proceed to change your password")
        win = Toplevel()
        changepassword.ChangePassword(win)
        self.window.withdraw()
        win.deiconify

    def click_signin(self):
        win = Toplevel()
        self.window.withdraw()
        signin.Signin(win)
        win.deiconify



    def on_closing(self):
        self.window.deiconify()
        ask = messagebox.askyesnocancel("Confirm exit", "Do you want to exit?")
        if ask is True:
            quit()

def win():
    window = Tk()
    ForgotPassword(window)
    window.mainloop()


if __name__ == '__main__':
    win()