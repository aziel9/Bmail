# import tkinter as tk

# def check_username():
#     username = username_entry.get()
#     if username == "":
#         error_label.config(text="Username cannot be empty", fg="red")
#     else:
#         error_label.config(text="", fg="black")

# root = tk.Tk()

# # create username label and entry
# username_label = tk.Label(root, text="Username:")
# username_label.pack()
# username_entry = tk.Entry(root)
# username_entry.pack()

# # create check button
# check_button = tk.Button(root, text="Check", command=check_username)
# check_button.pack()

# # create error label
# error_label = tk.Label(root, text="")
# error_label.pack()

# root.mainloop()

# from tkinter import *

# root = Tk()
# root.geometry("400x300")

# # Create username and password labels and entry fields
# Label(root, text="Username:").grid(row=0, column=0, padx=10, pady=10)
# username_entry = Entry(root)
# username_entry.grid(row=0, column=1, padx=10, pady=10)

# Label(root, text="Password:").grid(row=1, column=0, padx=10, pady=10)
# password_entry = Entry(root, show="*")
# password_entry.grid(row=1, column=1, padx=10, pady=10)

# # Define function to validate entries
# def validate_entries():
#     # Clear any existing error messages
#     error_label.config(text="")

#     # Check if username or password entry is empty
#     if not username_entry.get() or not password_entry.get():
#         # Display error message at the bottom of the corresponding field
#         if not username_entry.get():
#             error_label.config(text="Please enter a username.", anchor="w")
#             error_label.grid(row=2, column=1, sticky="w", padx=10)
#         if not password_entry.get():
#             error_label.config(text="Please enter a password.", anchor="w")
#             error_label.grid(row=3, column=1, sticky="w", padx=10)
#     else:
#         # Perform other actions if both fields are filled
#         pass

# # Create check button to validate entries
# check_button = Button(root, text="Check", command=validate_entries)
# check_button.grid(row=2, column=0, padx=10, pady=10)

# # Create error label for displaying error messages
# error_label = Label(root, fg="red")

# root.mainloop()

import tkinter as tk

class LoginPage(tk.Frame):
    def __init__(self, master, login_callback):
        super().__init__(master)
        self.login_callback = login_callback
        
        self.username_label = tk.Label(self, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()
        
        self.password_label = tk.Label(self, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()
        
        self.login_button = tk.Button(self, text="Login", command=self.login)
        self.login_button.pack()
        
    def login(self):
        # In a real implementation, you would verify the username and password against a database
        # Here, we'll just assume the username is "user" and the password is "password"
        if self.username_entry.get() == "user" and self.password_entry.get() == "password":
            # Call the login callback with the username
            self.login_callback(self.username_entry.get())
        else:
            tk.messagebox.showerror("Error", "Incorrect username or password")

class WelcomePage(tk.Frame):
    def __init__(self, master, username):
        super().__init__(master)
        
        welcome_label = tk.Label(self, text=f"Welcome, {username}!")
        welcome_label.pack()

def login_success(username):
    # Destroy the login page and create the welcome page
    login_page.destroy()
    welcome_page = WelcomePage(root, username)
    welcome_page.pack()

# Create the root window and the login page
root = tk.Tk()
login_page = LoginPage(root, login_success)
login_page.pack()

# Start the main event loop
root.mainloop()





