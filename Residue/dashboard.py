
from tkinter import *   
from PIL import ImageTk
from tkinter import messagebox
from datetime import *
import time
import re
import socket
import ast

class Homepage:
    def __init__(self, window, email, name):
        self.window = window
        self.window.geometry("1366x720+250+100")
        self.window.title("Login Page")
        self.window.resizable(False, False)

        self.currentusr_name = name
        self.currentusr_email = email

        self.dashboard_img= ImageTk.PhotoImage \
            (file="images\\dashboard2.png")
        self.image_panel = Label(self.window, image=self.dashboard_img)
        self.image_panel.pack(fill='both', expand='yes')

        #self.heading = Label(self.window, text='I-Message", font=('Times', 20, "bold"), bg="white",
        #             fg='Black', bd=5, relief=FLAT)
        #self.heading.place(x=350, y=26, width=550)
        
        ########## ON PRESSING X BUTTON TO CLOSE #############
        self.window.protocol("WM_DELETE_WINDOW", self.click_exit)

        self.clock_image = ImageTk.PhotoImage \
                            (file="images\\time.png")
        self.date_time_image = Label(self.window, image=self.clock_image, bg="white")
        self.date_time_image.place(x=35, y=45)
        self.date_time = Label(self.window)
        self.date_time.place(x=65, y=35)
        self.time_running()

        self.user_image = ImageTk.PhotoImage \
                            (file="images\\user.png")
        self.user_label = Label(self.window, image=self.user_image, bg="white")
        self.user_label.place(x=1000, y=47)
        #self.current_user = Label(self.window, text="(username)", bg="white", font=("Times", 10, "bold"),fg="green")
        self.current_user = Label(self.window, bg="white", font=("Times", 12, "bold"),fg="red")
        self.current_user.configure(text=self.currentusr_email)
        self.current_user.place(x=1030, y=48)

        self.logout_img = ImageTk.PhotoImage \
                            (file="images\\logout.png")
        self.logout_button = Button(self.window, image=self.logout_img, font=("yu gothic ui", 13, "bold"), relief=FLAT, activebackground="white"
                      , borderwidth=0, background="white", cursor="hand2", command=self.click_logout)
        self.logout_button.place(x=1241, y=50)

        self.home_img = ImageTk.PhotoImage \
                           (file="images\\home.png")
        self.home_button = Button(self.window, image=self.home_img, font=("Times", 13, "bold"), relief=FLAT,
                   activebackground="white", borderwidth=0, background="white", cursor="hand2", command=self.click_home)

        self.home_button.place(x=46, y=115)
        self.click_home()

        self.compose_img = ImageTk.PhotoImage \
                            (file="images\\compose.png")
        self.compose_button = Button(self.window, image=self.compose_img, font=("Times", 13, "bold"), relief=FLAT,
                   activebackground="white", borderwidth=0, background="white", cursor="hand2", command=self.click_compose)
        self.compose_button.place(x=46, y=240)

        self.inbox_img = ImageTk.PhotoImage \
                        (file="images\\inbox.png")
        self.inbox_button = Button(self.window, image=self.inbox_img, font=("Times", 13, "bold"), relief=FLAT,
                   activebackground="white", borderwidth=0, background="white", cursor="hand2", command=self.click_inbox)
        self.inbox_button.place(x=46, y=360)

        self.sent_img = ImageTk.PhotoImage \
                        (file="images\\sent.png")
        self.sent_button = Button(self.window, image=self.sent_img, font=("Times", 13, "bold"), relief=FLAT,
                   activebackground="white", borderwidth=0, background="white", cursor="hand2")#, command=self.click_sent)
        self.sent_button.place(x=46, y=480)

        self.exit_img = ImageTk.PhotoImage \
                        (file="images\\exit.png")
        self.exit_button = Button(self.window, image=self.exit_img, font=("Times", 13, "bold"), relief=FLAT,
                   activebackground="white", borderwidth=0, background="white", cursor="hand2", command=self.click_exit)
        self.exit_button.place(x=46, y=600)

    def time_running(self):
        self.time = time.strftime("%H:%M:%S")
        self.date = time.strftime('%Y-%m-%d')
        self.concated_time = f"  {self.time} \n {self.date}"
        self.date_time.configure(text=self.concated_time, font=("Times", 13, "bold"), relief=FLAT
                                 , borderwidth=0, background="white", foreground="#3a484c")
        self.date_time.after(100,self.time_running)

    
    def click_logout(self):
        import login
        ask = messagebox.askyesnocancel("Confirm Logout", "Do you want to logout?")
        if ask is True:
            self.currentusr_email= None
            self.currentusr_name= None
            win = Toplevel()
            login.Login(win)
            self.window.withdraw()
            win.deiconify()

    
    def click_home(self):
        self.window.title("Home")
        self.home_frame = Frame(self.window)
        self.home_frame.place(x=145, y=105, height=576, width=1181)
        self.home_frame_img= ImageTk.PhotoImage \
            (file='images\\home_frame.png')
        self.home_panel = Label(self.home_frame, image=self.home_frame_img, bg="white")
        self.home_panel.pack(fill='both', expand='yes')
        self.homeheading = Label(self.window,  font=("Times", 16,), bg="white", fg='red', relief=FLAT)
        self.homeheading.place(x=212, y=140, width=450)
        self.homeheading.configure(text=f"Welcome {self.currentusr_name}")

    def click_compose(self):
        self.window.title("Compose new message")
        self.compose_frame = Frame(self.window, bg="white")
        self.compose_frame.place(x=145, y=105, height=576, width=1181)
        self.compose_frame_img = ImageTk.PhotoImage \
                            (file="images\\composebg1.png")
        self.compose_label = Label(self.compose_frame, image=self.compose_frame_img, bg="white")
        self.compose_label.pack(fill='both', expand='yes')
        self.heading = Label(self.window, text="Compose new message", font=("Times", 16,), bg="white", fg='red', relief=FLAT)
        self.heading.place(x=217, y=140, width=450)
        self.toemail_label = Label(self.window, text="To: ", bg="white", fg="black",font=("Times", 12, "bold"))
        self.toemail_label.place(x=345, y=196)
        self.toemail_entry = Entry(self.window, highlightthickness=0, relief=FLAT, bg="white", fg="black",font=("Times", 12, "bold"))
        self.toemail_entry.place(x=385, y=197, width=440)
        self.subject_label = Label(self.window, text="Subject: ", bg="white", fg="black",font=("Times", 12, "bold"))
        self.subject_label.place(x=345, y=245)
        self.subject_entry = Entry(self.window, highlightthickness=0, relief=FLAT, bg="white", fg="black",font=("Times", 12, "bold"))
        self.subject_entry.place(x=424, y=246, width=400)
        self.message_label = Label(self.window, text="Message", bg="white", fg="black",font=("Times", 12, "bold"))
        self.message_label.place(x=345, y=288)
        self.message_entry =Text(self.window, highlightthickness=0 ,relief=FLAT, bg="white", fg="black",font=("yu gothic ui semibold", 12))
        self.message_entry.place(x=320, y=330,height=300, width=828)
        self.scrollbar = Scrollbar(self.window, orient='vertical', cursor="hand2")
        self.message_entry.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.message_entry.yview)
        self.scrollbar.place(x=1145, y=328, height=298)
        
        self.send_img = ImageTk.PhotoImage \
            (file="images\\send.png")
        self.send_button = Button(self.window, image=self.send_img, font=("Times", 13, "bold"), relief=FLAT, activebackground="white"
                      , borderwidth=0, background="white", cursor="hand2",command=self.click_send)
        self.send_button.place(x=1185, y=585)

    def click_send(self):
        try:
            if self.toemail_entry.get() == "":
                messagebox.showerror("Empty field","Enter receiver email id")
            elif self.is_valid_email() is False:
                messagebox.showerror("Error", "Invalid receiver email format")
            elif self.toemail_entry.get() == self.currentusr_email:
                messagebox.showerror("Error","Cannot send an email to yourself!")
            elif self.subject_entry.get() == "":
                messagebox.showerror("Empty field","Enter subject")
            elif self.message_entry.get("1.0", "end-1c") == "":
                messagebox.showerror("Empty field","Empty message field")
            else:
                ask = messagebox.askyesno("Confirm","Send this message?")
                if ask is True:
                    self.send()
                else:
                    pass
            
        except BaseException as msg:
            messagebox.showerror("Error","Enter all the fields")
            print(msg)
    
    def send(self):
        try:
            self.connect()
            time= datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
            sender= self.currentusr_email
            receiver= self.toemail_entry.get()
            subject= self.subject_entry.get()
            message= self.message_entry.get("1.0", "end-1c")
            # message = message.replace("\n", "\n\n")
            self.c.send(f"message|{time}|{sender}|{receiver}|{subject}|{message}".encode())
            response = self.c.recv(2048).decode()
            if response == "no_receiver":
                messagebox.showerror("Error","No receiver found")
            elif response == "message_not_sent":
                messagebox.showerror("Error","Message not sent. Try again later")
            elif response == "message_sent":
                messagebox.showinfo("Success","Email sent")
                self.toemail_entry.delete(0, END)
                self.subject_entry.delete(0, END)
                self.message_entry.delete("1.0", END)

        except BaseException as msg:
            messagebox.showerror("Fail","Could not send an email.")
            print(msg)


    def click_inbox(self):
        try:
            self.window.title("Inbox")
            self.inbox_list= Listbox(self.window, relief=RAISED, highlightthickness=0, bg="white")
            self.inbox_list.place(x=145, y=105, height=576, width=1181)

            self.connect()
            self.c.send(f"view_inbox|{self.currentusr_email}".encode())
            response = self.c.recv(2048).decode()
            response= response.split("|")
            response_type = response[0]

            if response_type == "empty_inbox":
                messagebox.showinfo("Empty", "No messages in inbox")
            elif response_type == "error":
                messagebox.showerror("Error","Error fetching inbox")
            elif response_type == "inbox":
                self.inbox_list.delete(0,END)
                message_data= response[1]
                message_metadata = ast.literal_eval(message_data)
                for message in message_metadata:
                    self.inbox_list.insert(END, message[3])


        except BaseException as msg:
            print("Error:",msg)
            pass



    def is_valid_email(self):
        pattern = r"^[a-z][a-z0-9]*@login\.com$"
        if re.match(pattern, self.toemail_entry.get()):
            return True
        return False

    def click_exit(self):
        self.window.deiconify()
        ask = messagebox.askyesnocancel("Confirm exit", "Do you want to exit?")
        if ask is True:
            quit()

    def connect(self):
        try:
            self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.host = socket.gethostname()
            #self.host= "192.168.1.8"	
            self.port = 1234			
            self.c.connect((self.host,self.port))

        except BaseException as msg:
            messagebox.showerror("Connection failure","Failed to connect with server")
            print(msg)

def win():
    window = Tk()
    Homepage(window)
    window.mainloop()

if __name__ == '__main__':
    win()