from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
import signin
import re
import socket

class ChangePassword:
    def __init__(self,window):
        self.window = window
        self.window.geometry("1906x952+5+9")
        self.window.title("Change Password")
        self.window.resizable(False, False)
        
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
        pass

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
    ChangePassword(window)
    window.mainloop()


if __name__ == '__main__':
    win()