from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
import re
import create
import socket


class VerifyOTP:
    def __init__(self, window):
        self.window = window
        self.window.geometry("1906x952+5+9")
        self.window.title("Verify")
        self.window.resizable(False, False)

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
                                   , borderwidth=0, background="white", cursor="hand2", command=self.click_cancel)
        self.cancel_button.place(x=969, y=619)

    def click_verify(self):
        try:
            if self.valid_otp() is False:
                messagebox.askokcancel("OTP","OTP should be six digit numbers only")
            else:
                self.verified()
        except BaseException as msg:
            print(msg)

    def verified(self):
        messagebox.showinfo("Success","Account has been created")

        

    def click_cancel(self):
        win = Toplevel()
        self.window.withdraw()
        create.Signup(win)
        win.deiconify()
        

    def valid_otp(self):
        pattern = r"^[0-9]{6}$"
        if re.match(pattern, self.otp_entry.get()):
            return True
        return False

    
    def on_closing(self):
        self.window.deiconify()
        ask = messagebox.askyesnocancel("Confirm exit", "Do you want to exit?")
        if ask is True:
            quit()



def win():
    window = Tk()
    VerifyOTP(window)
    window.mainloop()


if __name__ == '__main__':
    win()