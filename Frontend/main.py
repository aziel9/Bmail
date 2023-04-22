from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
from datetime import *
import json

class Home:
    def __init__(self,window,email,name,socket_connection):
        self.window = window
        self.window.geometry("1906x952+5+9")
        self.window.title("Home")
        self.window.resizable(False, False)

        self.currentusr_email = email
        self.currentusr_name = name
        self.socket_connection = socket_connection

        ########## ON PRESSING X BUTTON TO CLOSE #############
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.background_img=ImageTk.PhotoImage \
            (file="images\\homeframe.png")
        self.background_image_panel = Label(self.window, image=self.background_img)
        self.background_image_panel.pack(fill='both', expand='yes')

        self.bmail_logo = ImageTk.PhotoImage \
            (file="images\\bmail.png")
        self.bmail_logo_panel = Label(self.window, image=self.bmail_logo, relief=FLAT, background="white", borderwidth=0)
        self.bmail_logo_panel.place(x=60, y=25)

        self.menu_img= ImageTk.PhotoImage \
            (file="images\\menu.png")
        self.menu_panel = Label(self.window, image=self.menu_img, relief=FLAT, background="white", borderwidth=0)
        self.menu_panel.place(x=50, y=163)

        self.home_img = ImageTk.PhotoImage \
            (file="images\\home.png")
        self.homehov_img = ImageTk.PhotoImage \
            (file="images\\homehov.png")
        self.home_button = Button(self.window, image=self.home_img, relief=FLAT, activebackground="white"
                                   , borderwidth=0, background="white", cursor="hand2", command=self.click_home)
        self.home_button.place(x=94, y=216)

        self.compose_img = ImageTk.PhotoImage \
            (file="images\\compose.png")
        self.composehov_img = ImageTk.PhotoImage \
            (file="images\\composehov.png")
        self.compose_button = Button(self.window, image=self.compose_img, relief=FLAT, activebackground="white"
                                   , borderwidth=0, background="white", cursor="hand2", command=self.click_compose)
        self.compose_button.place(x=94, y=277)

        self.inbox_img = ImageTk.PhotoImage \
            (file="images\\inbox.png")
        self.inboxhov_img = ImageTk.PhotoImage \
            (file="images\\inboxhov.png")
        self.inbox_button = Button(self.window, image=self.inbox_img, relief=FLAT, activebackground="white"
                                   , borderwidth=0, background="white", cursor="hand2", command=self.click_inbox)
        self.inbox_button.place(x=94, y=338)

        self.sent_img = ImageTk.PhotoImage \
            (file="images\\sent.png")
        self.senthov_img = ImageTk.PhotoImage \
            (file="images\\senthov.png")
        self.sent_button = Button(self.window, image=self.sent_img, relief=FLAT, activebackground="white"
                                   , borderwidth=0, background="white", cursor="hand2", command=self.click_sent)
        self.sent_button.place(x=94, y=399)

        self.starred_img = ImageTk.PhotoImage \
            (file="images\\starred.png")
        self.starredhov_img = ImageTk.PhotoImage \
            (file="images\\starredhov.png")
        self.starred_button = Button(self.window, image=self.starred_img, relief=FLAT, activebackground="white"
                                   , borderwidth=0, background="white", cursor="hand2", command=self.click_starred)
        self.starred_button.place(x=94, y=460)

        self.settings_img= ImageTk.PhotoImage \
            (file="images\\settings.png")
        self.settings_panel = Label(self.window, image=self.settings_img, relief=FLAT, background="white", borderwidth=0)
        self.settings_panel.place(x=50, y=533)

        self.myprofile_img = ImageTk.PhotoImage \
            (file="images\\myprofile.png")
        self.myprofilehov_img = ImageTk.PhotoImage \
            (file="images\\myprofilehov.png")
        self.myprofile_button = Button(self.window, image=self.myprofile_img, relief=FLAT, activebackground="white"
                                   , borderwidth=0, background="white", cursor="hand2", command=self.click_myprofile)
        self.myprofile_button.place(x=94, y=594)

        self.password_img = ImageTk.PhotoImage \
            (file="images\\pass.png")
        self.passwordhov_img = ImageTk.PhotoImage \
            (file="images\\passhov.png")
        self.password_button = Button(self.window, image=self.password_img, relief=FLAT, activebackground="white"
                                   , borderwidth=0, background="white", cursor="hand2", command=self.click_password)
        self.password_button.place(x=94, y=655)

        self.logout_img = ImageTk.PhotoImage \
            (file="images\\logout.png")
        self.logouthov_img = ImageTk.PhotoImage \
            (file="images\\logouthov.png")
        self.logout_button = Button(self.window, image=self.logout_img, relief=FLAT, activebackground="white"
                                   , borderwidth=0, background="white", cursor="hand2", command=self.click_logout)
        self.logout_button.place(x=94, y=716)
        
        self.currentuser_img= ImageTk.PhotoImage \
            (file="images\\user.png")
        self.currentuser = Label(self.window, image=self.currentuser_img, relief=FLAT, background="#ECEBFF", borderwidth=0)
        self.currentuser.place(x=1615, y=19)

        self.currentuser_heading = Label(self.window, font=("Inter", 11, "bold"), bg="#ECEBFF", fg='black')
        self.currentuser_heading.place(x=1675, y=30)
        self.currentuser_heading.configure(text=self.currentusr_name)

        self.home_button.bind("<Enter>", lambda e: on_enter(self.home_button, self.homehov_img))
        self.home_button.bind("<Leave>", lambda e: on_leave(self.home_button, self.home_img))
        self.compose_button.bind("<Enter>", lambda e: on_enter(self.compose_button, self.composehov_img))
        self.compose_button.bind("<Leave>", lambda e: on_leave(self.compose_button, self.compose_img))
        self.inbox_button.bind("<Enter>", lambda e: on_enter(self.inbox_button, self.inboxhov_img))
        self.inbox_button.bind("<Leave>", lambda e: on_leave(self.inbox_button, self.inbox_img))
        self.sent_button.bind("<Enter>", lambda e: on_enter(self.sent_button, self.senthov_img))
        self.sent_button.bind("<Leave>", lambda e: on_leave(self.sent_button, self.sent_img))
        self.starred_button.bind("<Enter>", lambda e: on_enter(self.starred_button, self.starredhov_img))
        self.starred_button.bind("<Leave>", lambda e: on_leave(self.starred_button, self.starred_img))
        self.myprofile_button.bind("<Enter>", lambda e: on_enter(self.myprofile_button, self.myprofilehov_img))
        self.myprofile_button.bind("<Leave>", lambda e: on_leave(self.myprofile_button, self.myprofile_img))
        self.password_button.bind("<Enter>", lambda e: on_enter(self.password_button, self.passwordhov_img))
        self.password_button.bind("<Leave>", lambda e: on_leave(self.password_button, self.password_img))
        self.logout_button.bind("<Enter>", lambda e: on_enter(self.logout_button, self.logouthov_img))
        self.logout_button.bind("<Leave>", lambda e: on_leave(self.logout_button, self.logout_img))

        def on_enter(button, hover_img):
            button.configure(image=hover_img)

        def on_leave(button, normal_img):
            button.configure(image=normal_img)

        self.current_frame = None

    ######################################################################
    ########################   H O M E   #################################
    ######################################################################

    def click_home(self):
        pass

    ######################################################################
    #####################   C O M P O S E    #############################
    ######################################################################

    def click_compose(self):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.window.title("Compose")

        self.compose_frame_img = ImageTk.PhotoImage \
                            (file="images\\composeframe.png")
        self.current_frame = Label(self.window, image=self.compose_frame_img, bg="#ECEBFF")
        self.current_frame.place(x=532, y=106)
        self.star_img = ImageTk.PhotoImage \
                            (file="images\\star.png")
        self.star_frame_label = Label(self.current_frame, image=self.star_img, bg="white")
        self.star_frame_label.place(x=84,y=27)
        self.compose_heading = Label(self.current_frame, text="New Message", font=("Inter", 14, "bold"), bg="white", fg='#000000')
        self.compose_heading.place(x=128, y=27)

        self.fromemail_label = Label(self.current_frame, text="From: ", bg="white", fg="black",font=("Inter", 12))
        self.fromemail_label.place(x=84, y=119)
        self.fromemail_entry = Entry(self.current_frame, highlightthickness=0, relief=FLAT,bg="white", fg="black",font=("Inter", 12), readonlybackground='white')
        self.fromemail_entry.place(x=180, y=124, width=465)
        self.fromemail_entry.insert(0,f'{self.currentusr_email}')
        self.fromemail_entry.configure(state='readonly')

        self.toemail_label = Label(self.current_frame, text="To: ", bg="white", fg="black",font=("Inter", 12))
        self.toemail_label.place(x=84, y=198)
        self.toemail_entry = Entry(self.current_frame, highlightthickness=0, relief=FLAT, bg="white", fg="black",font=("Inter", 12))
        self.toemail_entry.place(x=180, y=204, width=465)

        self.subject_entry = Entry(self.current_frame, highlightthickness=0, relief=FLAT, bg="white", fg="black",font=("Inter", 12,"bold"))
        self.subject_entry.place(x=93, y=286, width=790)
        self.subject_entry.insert(0, 'Subject:')
        self.subject_entry.bind('<FocusIn>',self.on_entersubj)
        self.subject_entry.bind('<FocusOut>',self.on_leavesubj)

        self.message_entry =Text(self.current_frame, highlightthickness=0 ,wrap="word",padx=11,relief=FLAT, bg="white", fg="black",font=("Inter", 12))
        self.message_entry.place(x=92, y=368,height=365, width=1046)
        self.message_entry.bind("<<Paste>>", self.on_message_paste)

        self.scrollbar = Scrollbar(self.current_frame, orient='vertical', cursor="hand2", width=15)
        self.message_entry.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.message_entry.yview)
        self.scrollbar.place(x=1128, y =368, height =365)
        
        self.send_img = ImageTk.PhotoImage \
            (file="images\\send.png")
        self.send_button = Button(self.current_frame, image=self.send_img, relief=FLAT, activebackground="white"
                                   , borderwidth=0, background="white", cursor="hand2", command=self.click_send)
        self.send_button.place(x=963, y=750)

    def on_message_paste(self, event):
        self.message_entry.update_idletasks()
        self.message_entry.see("end")

    def on_entersubj(self, event):
        enter_subj=self.subject_entry.get()
        if enter_subj == 'Subject:':
            self.subject_entry.delete(0, 'end')
        
    def on_leavesubj(self, event):
        enter_subj=self.subject_entry.get()
        if enter_subj == "":
            self.subject_entry.insert(0, 'Subject:')

    def click_send(self):
        if not self.fromemail_entry.get():
            messagebox.showerror("Empty field","Empty sender address")
        elif not self.toemail_entry.get():
            messagebox.showerror("Empty field", "Enter receipent address")
        elif self.toemail_entry.get() == self.fromemail_entry.get():
            messagebox.showerror("Invalid address","You are trying to send mail to yourself")
        elif self.subject_entry.get() == "Subject:":
            messagebox.showerror("Empty field","Enter subject of your message")
        elif not self.message_entry.get("1.0", "end-1c"):
            messagebox.showerror("Empty field","Enter your message")
        else:
            try:
                self.socket_connection.connect()
                request = {
                    'type': 'check_receipent',
                    'receipentid': self.toemail_entry.get() ,
                }
                request_json = json.dumps(request)
                self.socket_connection.send(request_json)
                response_json = self.socket_connection.receive()
                response = json.loads(response_json)
                # self.socket_connection.send(request)
                # response = self.socket_connection.receive()
                if response['type'] == "receipent_exists":
                    receivername = response['receivername']
                    print(receivername)
                    self.socket_connection.connect()
                    request = {
                        'type': 'client_message',
                        'sendername': self.currentusr_name,
                        'senderid': self.currentusr_email,
                        'receivername': receivername,
                        'receiverid': self.toemail_entry.get(),
                        'subject': self.subject_entry.get(),
                        'body': self.message_entry.get("1.0", "end-1c")
                    }
                    request_json = json.dumps(request)
                    self.socket_connection.send(request_json)
                    response_json = self.socket_connection.receive()
                    response = json.loads(response_json)
                    if response['type'] =="message_sent":
                        self.toemail_entry.delete(0, END)
                        self.subject_entry.delete(0, END)
                        self.message_entry.delete("1.0", END)
                        messagebox.showinfo("Message sent","Message sent successfully")
                    elif response['type'] == "message_sent_failed":
                        messagebox.showerror("Failed","Failed to send a message")
                elif response['type'] == "no_receipent":
                    messagebox.showerror("Invalid receipent","Receipent address doesnot exists")
                elif response['type'] == "error":
                    messagebox.showerror("Server issue","Server is Disconnected")
            except ConnectionRefusedError as msg:
                messagebox.showerror("Connection Failure","Failed to establish connection with server.")
                print(msg)

    ######################################################################
    ######################   I N B O X   #################################
    ######################################################################

    def click_inbox(self):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.window.title("Inbox")
        self.current_frame = Frame(self.window, bg="#ECEBFF")
        self.current_frame.place(x=413, y=98, width=1480, height=837)

        self.inboxlist_frame_img = ImageTk.PhotoImage \
                            (file="images\\list.png")
        self.inboxlist_label = Label(self.current_frame, image=self.inboxlist_frame_img, bg="#ECEBFF")
        self.inboxlist_label.place(x=0, y=0)
        self.inbox_listbox = Listbox(self.inboxlist_label,background='red')
        # inbox_listbox.bind("<<ListboxSelect>>", show_message)
        self.inbox_listbox.place(x=30,y=90, width=455, height=710)
        
        self.starinb_img = ImageTk.PhotoImage \
                            (file="images\\star.png")
        self.starinb_frame_label = Label(self.inboxlist_label, image=self.starinb_img, bg="white")
        self.starinb_frame_label.place(x=84,y=27)
        self.inbox_heading = Label(self.inboxlist_label, text="Inbox", font=("Inter", 14, "bold"), bg="white", fg='#000000')
        self.inbox_heading.place(x=128, y=27)

        self.inboxbx_frame_img = ImageTk.PhotoImage \
                            (file="images\\box.png")
        self.inboxbx_label = Label(self.current_frame, image=self.inboxbx_frame_img, bg="#ECEBFF")
        self.inboxbx_label.place(x=527, y=0)
        self.inboxbody_frame = Label(self.inboxbx_label, background='red')
        self.inboxbody_frame.place(x=18, y=18, width=906, height=788)
        self.body_text = Text(self.inboxbody_frame)
        self.body_text.pack(side="left", fill="both", expand=True)
        # try:
        #     self.socket_connection.connect()
        #     self.socket_connection.send(f"request_inbox_message|{self.currentusr_email}")
        #     response = self.socket_connection.receive()
        #     if response == "empty_inbox":
        #         messagebox.showerror("Empty Inbox","Your inbox is empty")
        #     elif response == "error":
        #         messagebox.showerror("Server issue","Server is disconnected")
        #     else:
        #         pass

        # except BaseException as msg:
        #     print(msg)

    ######################################################################
    #######################   S E N T   ##################################
    ######################################################################

    def click_sent(self):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.window.title("Sent")
        self.current_frame = Frame(self.window, bg="#ECEBFF")
        self.current_frame.place(x=413, y=98, width=1480, height=837)

        self.starredlist_frame_img = ImageTk.PhotoImage \
                            (file="images\\list.png")
        self.starredlist_label = Label(self.current_frame, image=self.starredlist_frame_img, bg="#ECEBFF")
        self.starredlist_label.place(x=0, y=0)
        self.starstarred_img = ImageTk.PhotoImage \
                            (file="images\\star.png")
        self.starstarred_frame_label = Label(self.starredlist_label, image=self.starstarred_img, bg="white")
        self.starstarred_frame_label.place(x=84,y=27)
        self.starred_heading = Label(self.starredlist_label, text="Sent", font=("Inter", 14, "bold"), bg="white", fg='#000000')
        self.starred_heading.place(x=128, y=27)

        self.starredbx_frame_img = ImageTk.PhotoImage \
                            (file="images\\box.png")
        self.starredbx_label = Label(self.current_frame, image=self.starredbx_frame_img, bg="#ECEBFF")
        self.starredbx_label.place(x=527, y=0)


    ######################################################################
    #####################   S T A R R E D   ##############################
    ###################################################################### 

    def click_starred(self):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.window.title("Starred")
        self.current_frame = Frame(self.window, bg="#ECEBFF")
        self.current_frame.place(x=413, y=98, width=1480, height=837)

        self.starredlist_frame_img = ImageTk.PhotoImage \
                            (file="images\\list.png")
        self.starredlist_label = Label(self.current_frame, image=self.starredlist_frame_img, bg="#ECEBFF")
        self.starredlist_label.place(x=0, y=0)
        self.starstarred_img = ImageTk.PhotoImage \
                            (file="images\\star.png")
        self.starstarred_frame_label = Label(self.starredlist_label, image=self.starstarred_img, bg="white")
        self.starstarred_frame_label.place(x=84,y=27)
        self.starred_heading = Label(self.starredlist_label, text="Starred", font=("Inter", 14, "bold"), bg="white", fg='#000000')
        self.starred_heading.place(x=128, y=27)

        self.starredbx_frame_img = ImageTk.PhotoImage \
                            (file="images\\box.png")
        self.starredbx_label = Label(self.current_frame, image=self.starredbx_frame_img, bg="#ECEBFF")
        self.starredbx_label.place(x=527, y=0)


    ######################################################################
    #####################   P R O F I L E   ##############################
    ######################################################################   

    def click_myprofile(self):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.window.title("My Profile")
        self.myprofile_frame_img = ImageTk.PhotoImage \
                            (file="images\\myprofileframe.png")
        self.current_frame = Label(self.window, image=self.myprofile_frame_img, bg="#ECEBFF")
        self.current_frame.place(x=532, y=106)

        self.myname_heading = Label(self.current_frame, font=("Inter", 16, "bold"), bg="white", fg='#000000')
        self.myname_heading.place(x=281, y=67)
        self.bmail_heading = Label(self.current_frame, font=("Inter", 12), bg="white", fg='#000000')
        self.bmail_heading.place(x=281, y=125)
        self.changepic_img = ImageTk.PhotoImage \
            (file="images\\changepic.png")
        self.changepic_button = Button(self.current_frame, image=self.changepic_img, relief=FLAT, activebackground="white"
                                   , borderwidth=0, background="white", cursor="hand2")#, command=self.click_send)
        self.changepic_button.place(x=281, y=176)

        self.myprofmob_img = ImageTk.PhotoImage \
                            (file="images\\myprofilemobile.png")
        self.myprofmob_label = Label(self.current_frame, image=self.myprofmob_img, bg="white")
        self.myprofmob_label.place(x=83,y=279)
        self.myprofmob_heading = Label(self.current_frame, font=("Inter", 13), bg="white", fg='#000000')
        self.myprofmob_heading.place(x=140, y=279)

        self.myprofdob_img = ImageTk.PhotoImage \
                            (file="images\\myprofilebday.png")
        self.myprofdob_label = Label(self.current_frame, image=self.myprofdob_img, bg="white")
        self.myprofdob_label.place(x=83,y=343)
        self.myprofdob_heading = Label(self.current_frame, font=("Inter", 13), bg="white", fg='#000000')
        self.myprofdob_heading.place(x=145, y=345)

        self.myprofgender_img = ImageTk.PhotoImage \
                            (file="images\\myprofilegender.png")
        self.myprofgender_label = Label(self.current_frame, image=self.myprofgender_img, bg="white")
        self.myprofgender_label.place(x=83,y=407)
        self.myprofgender_heading = Label(self.current_frame, font=("Inter", 13), bg="white", fg='#000000')
        self.myprofgender_heading.place(x=145, y=407)

        self.myprofcountry_img = ImageTk.PhotoImage \
                            (file="images\\myprofilecountry.png")
        self.myprofcountry_label = Label(self.current_frame, image=self.myprofcountry_img, bg="white")
        self.myprofcountry_label.place(x=83,y=471)
        self.myprofcountry_heading = Label(self.current_frame, font=("Inter", 13), bg="white", fg='#000000')
        self.myprofcountry_heading.place(x=145, y=469)

        self.myprofdate_img = ImageTk.PhotoImage \
                            (file="images\\myprofiledate.png")
        self.myprofdate_label = Label(self.current_frame, image=self.myprofdate_img, bg="white")
        self.myprofdate_label.place(x=83,y=532)
        self.myprofdate_heading = Label(self.current_frame, font=("Inter", 13), bg="white", fg='#000000')
        self.myprofdate_heading.place(x=145, y=533)

        self.deleteacc_img = ImageTk.PhotoImage \
            (file="images\\deleteacc.png")
        self.deleteacc_button = Button(self.current_frame, image=self.deleteacc_img, relief=FLAT, activebackground="white"
                                   , borderwidth=0, background="white", cursor="hand2", command=self.click_deleteaccount)
        self.deleteacc_button.place(x=87, y=595)

        try:
            self.socket_connection.connect()
            request = {
                'type': 'view_profile',
                'email': self.currentusr_email
            }
            request_json = json.dumps(request)
            self.socket_connection.send(request_json)
            response_json = self.socket_connection.receive()
            response = json.loads(response_json)
            # self.socket_connection.send(request)
            # response = self.socket_connection.receive()
            if response['type'] == "error":
                messagebox.showerror("Server issue","Server disconnected")
            elif response['type'] == "my_profile":
                self.myname_heading.configure(text=f"{response['name']}")
                self.bmail_heading.configure(text=f"{response['email']}")
                self.myprofmob_heading.configure(text=f"{response['mobile']}")
                self.myprofdob_heading.configure(text=f"{response['bday']}")
                self.myprofgender_heading.configure(text=f"{response['gender']}")
                self.myprofcountry_heading.configure(text=f"Nepal")
                self.myprofdate_heading.configure(text=f"Account created on {response['accountdate']}") 
        except BaseException as msg:
            print(msg)

    def click_deleteaccount(self):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.window.title("Delete Account")
        self.cdelete_frame_img = ImageTk.PhotoImage \
                            (file="images\\cdeleteframe.png")
        self.current_frame = Label(self.window, image=self.cdelete_frame_img, bg="#ECEBFF")
        self.current_frame.place(x=760, y=106)

        self.bmaildel_logo = ImageTk.PhotoImage \
            (file="images\\bmail.png")
        self.bmail_logo_panel = Label(self.current_frame, image=self.bmaildel_logo, relief=FLAT, background="white", borderwidth=0)
        self.bmail_logo_panel.place(x=193, y=50)

        self.heading_deleteacc = Label(self.current_frame, text="Delete My Account? ", font=("Inter", 18, "bold"), bg="white", fg='#FF0000')
        self.heading_deleteacc.place(x=193, y=213)

        self.message_label1 = Label(self.current_frame, text="This will permanently delete all the account ", bg="white", fg="#000000", font=("Inter", 11, "bold"))
        self.message_label1.place(x=145, y=307)
        self.message_label2 = Label(self.current_frame, text="information from ", bg="white", fg="#000000", font=("Inter", 11, "bold"))
        self.message_label2.place(x=145, y=337)
        self.message_label3 = Label(self.current_frame, text="Bmail. ", bg="white", fg="#5356FB", font=("Inter", 11, "bold"))
        self.message_label3.place(x=297, y=337)
        self.message_label4 = Label(self.current_frame, text="However, the emails", bg="white", fg="#000000", font=("Inter", 11, "bold"))
        self.message_label4.place(x=355, y=337)
        self.message_label5 = Label(self.current_frame, text="are still stored in our system for other users to view.", bg="white", fg="#000000", font=("Inter", 11, "bold"))
        self.message_label5.place(x=116, y=367)

        self.currentpwd_label = Label(self.current_frame, text="Password", bg="white", fg="Black",font=("Inter", 11, "bold"))
        self.currentpwd_label.place(x=152, y=419)
        self.currentpwd_entry = Entry(self.current_frame, highlightthickness=0, relief=FLAT, bg="#EDEDED", fg="#000000",font=("Inter", 11, "bold"), show="*")
        self.currentpwd_entry.place(x=158, y=452, width=350, height=50)

        self.delbtn_img = ImageTk.PhotoImage \
            (file="images\\cdelete.png")
        self.delete_button = Button(self.current_frame, image=self.delbtn_img, relief=FLAT, activebackground="white"
                                   , borderwidth=0, background="white", cursor="hand2", command=self.click_deleteacc)
        self.delete_button.place(x=156, y=571)

        self.cancelbtn_img = ImageTk.PhotoImage \
            (file="images\\cancel.png")
        self.cancel_button = Button(self.current_frame, image=self.cancelbtn_img, relief=FLAT, activebackground="white"
                                   , borderwidth=0, background="white", cursor="hand2", command=self.click_myprofile)
        self.cancel_button.place(x=366, y=571)

    def click_deleteacc(self):
        if self.currentpwd_entry.get() == "":
            messagebox.showerror("Empty field","Enter password")
        else:
            try:
                self.socket_connection.connect()
                request = {
                    'type': 'delete_account',
                    'email': self.currentusr_email,
                    'password': self.currentpwd_entry.get()
                }
                request_json = json.dumps(request)
                self.socket_connection.send(request_json)
                response_json = self.socket_connection.receive()
                response = json.loads(response_json)
                # self.socket_connection.send(request)
                # response = self.socket_connection.receive()
                if response['type'] == "wrong_password":
                    messagebox.showerror("Wrong password","Password doesn't match with our system")
                elif response['type'] == "delete_account_success":
                    win = Toplevel()
                    self.window.withdraw()
                    DeleteAccount(win,self.socket_connection)
                    win.deiconify()
                elif response['type'] == "error":
                    messagebox.showerror("Server issue","Server is disconnected")
            except ConnectionRefusedError as msg:
                messagebox.showerror("Connection Failure","Failed to establish connection with server.")
                print(msg)

    ######################################################################
    ###################   P A S S W O R D   ##############################
    ######################################################################

    def click_password(self):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.window.title("Change Password")

        self.current_frame = Frame(self.window, bg="#ECEBFF")
        self.current_frame.place(x=770, y=106, width=675, height=828)
        self.changepassword_frame_img = ImageTk.PhotoImage \
                            (file="images\\updatepassframe.png")
        self.changepassword_label = Label(self.current_frame, image=self.changepassword_frame_img, bg="#ECEBFF")
        self.changepassword_label.pack()

        self.bmailpass_logo = ImageTk.PhotoImage \
            (file="images\\bmail.png")
        self.bmail_logo_panel = Label(self.changepassword_label, image=self.bmailpass_logo, relief=FLAT, background="white", borderwidth=0)
        self.bmail_logo_panel.place(x=193, y=50)

        self.heading_change = Label(self.changepassword_label, text="Change ", font=("Inter", 18, "bold"), bg="white", fg='#000000')
        self.heading_change.place(x=200, y=207)
        self.heading_pass = Label(self.changepassword_label, text="password?", font=("Inter", 18, "bold"), bg="white", fg='#FF0000')
        self.heading_pass.place(x=318, y=207)

        self.currentpassword_label = Label(self.changepassword_label, text="Current password", bg="white", fg="#000000", font=("Inter", 11, "bold"))
        self.currentpassword_label.place(x=150, y=290)
        self.currentpassword_entry = Entry(self.changepassword_label, highlightthickness=0, relief=FLAT, bg="#EDEDED", fg="#000000",font=("Inter", 11, "bold"), show="*")
        self.currentpassword_entry.place(x=157, y=323, width=350, height=50)
        self.newpassword_label = Label(self.changepassword_label, text="New password", bg="white", fg="#000000", font=("Inter", 11, "bold"))
        self.newpassword_label.place(x=150, y=396)
        self.newpassword_entry = Entry(self.changepassword_label, highlightthickness=0, relief=FLAT, bg="#EDEDED", fg="#000000",font=("Inter", 11, "bold"), show="*")
        self.newpassword_entry.place(x=157, y=429, width=350, height=50)
        self.confirmpassword_label = Label(self.changepassword_label, text="Confirm password", bg="white", fg="#000000", font=("Inter", 11, "bold"))
        self.confirmpassword_label.place(x=150, y=500)
        self.confirmpassword_entry = Entry(self.changepassword_label, highlightthickness=0, relief=FLAT, bg="#EDEDED", fg="#000000",font=("Inter", 11, "bold"), show="*")
        self.confirmpassword_entry.place(x=157, y=533, width=350, height=50)
        self.change_img = ImageTk.PhotoImage \
            (file="images\\change.png")
        self.change_button = Button(self.changepassword_label, image=self.change_img, relief=FLAT, activebackground="white"
                                   , borderwidth=0, background="white", cursor="hand2", command=self.update_password)
        self.change_button.place(x=257, y=633)

    def update_password(self):
        if self.currentpassword_entry.get()=="":
            messagebox.showerror("Empty Field","Enter current password")
        elif self.newpassword_entry.get()=="":
            messagebox.showerror("Empty Field","Enter confirm password")
        elif self.confirmpassword_entry.get()=="":
            messagebox.showerror("Empty Field","Confirm password")
        elif self.newpassword_entry.get() != self.confirmpassword_entry.get():
            messagebox.showerror("Mismatch","Password Mismatch")
        else:
            try:
                self.socket_connection.connect()
                request = {
                    'type': 'update_password',
                    'email': self.currentusr_email ,
                    'password': self.currentpassword_entry.get(),
                    'newpassword': self.newpassword_entry.get()
                }
                request_json = json.dumps(request)
                self.socket_connection.send(request_json)
                response_json = self.socket_connection.receive()
                response = json.loads(response_json)
                # self.socket_connection.send(request)
                # response = self.socket_connection.receive()
                if response['type'] == "wrong_password":
                    messagebox.showerror("Wrong password","Current password doesn't  match with our system")
                elif response['type'] == "update_password_success":
                    self.currentpassword_entry.delete(0, END)
                    self.newpassword_entry.delete(0, END)
                    self.confirmpassword_entry.delete(0, END)
                    messagebox.showinfo("Success","Password has been changed.")
                elif response['type'] == "error":
                    messagebox.showerror("Server issue","Server is disconnected")
            except ConnectionRefusedError as msg:
                messagebox.showerror("Connection Failure","Failed to establish connection with server.")
                print(msg)

    ######################################################################
    #####################   L O G O U T   ################################
    ######################################################################

    def click_logout(self):
        from signin import Signin
        ask = messagebox.askyesnocancel("Confirm Logout", "Do you want to logout?")
        if ask is True:
            self.currentusr_email= None
            self.currentusr_name= None
            win = Toplevel()
            Signin(win, self.socket_connection)
            self.window.withdraw()
            win.deiconify()

    def on_closing(self):
        self.window.deiconify()
        ask = messagebox.askyesnocancel("Confirm exit", "Do you want to exit?")
        if ask is True:
            quit()

class DeleteAccount:
    def __init__(self,window, socket_connection):
        self.window = window
        self.window.geometry("1906x952+5+9")
        self.window.title("Account Deleted")
        self.window.resizable(False, False)

        self.socket_connection = socket_connection

        ########## ON PRESSING X BUTTON TO CLOSE #############
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.background_img=ImageTk.PhotoImage \
            (file="images\\deletedframe.png")
        self.deletedfr_panel = Label(self.window, image=self.background_img)
        self.deletedfr_panel.pack(fill='both', expand='yes')

        self.bmail_logo = ImageTk.PhotoImage \
            (file="images\\bmail.png")
        self.bmail_logo_panel = Label(self.window, image=self.bmail_logo, relief=FLAT, background="white", borderwidth=0)
        self.bmail_logo_panel.place(x=796, y=94)
        
        self.heading = Label(self.window, text="Account Deleted Successfully", font=("Inter", 16, "bold"), bg="white", fg='#FF0000')
        self.heading.place(x=730, y=324)

        self.message_label1 = Label(self.window, text="Your account has been ", bg="white", fg="#000000", font=("Inter", 11, "bold"))
        self.message_label1.place(x=777, y=456)
        self.message_label2 = Label(self.window, text="permanently", bg="white", fg="#FF0000", font=("Inter", 11, "bold"))
        self.message_label2.place(x=985, y=456)
        self.message_label3 = Label(self.window, text="deleted from our ", bg="white", fg="#000000", font=("Inter", 11, "bold"))
        self.message_label3.place(x=814, y=490)
        self.message_label4 = Label(self.window, text="system.", bg="white", fg="#5356FB", font=("Inter", 11, "bold"))
        self.message_label4.place(x=969, y=490)

        self.ok_img = ImageTk.PhotoImage \
            (file="images\\ok.png")
        self.ok_button = Button(self.window, image=self.ok_img, relief=FLAT, activebackground="white"
                                   , borderwidth=0, background="white", cursor="hand2", command=self.click_ok)
        self.ok_button.place(x=860, y=611)

    def click_ok(self):
        from signin import Signin
        win = Toplevel()
        Signin(win, self.socket_connection)
        self.window.withdraw()
        win.deiconify()
   
    def on_closing(self):
        self.window.deiconify()
        ask = messagebox.askyesnocancel("Confirm exit", "Do you want to exit?")
        if ask is True:
            quit()

def win():
    window = Tk()
    Home(window)
    window.mainloop()

if __name__ == '__main__':
    win()