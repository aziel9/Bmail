import tkinter as tk
import random

class SignupPage(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        # Create widgets for signup page
        self.name_label = tk.Label(self, text="Name:")
        self.name_label.pack()
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()

        self.email_label = tk.Label(self, text="Email:")
        self.email_label.pack()
        self.email_entry = tk.Entry(self)
        self.email_entry.pack()

        self.phone_label = tk.Label(self, text="Phone Number:")
        self.phone_label.pack()
        self.phone_entry = tk.Entry(self)
        self.phone_entry.pack()

        self.signup_button = tk.Button(self, text="Sign up", command=self.open_verification)
        self.signup_button.pack()

    def open_verification(self):
        # Generate random verification code
        self.verification_code = str(random.randint(1000, 9999))

        # Hide signup page and create verification page
        self.pack_forget()
        VerificationPage(self.master, self.verification_code)

class VerificationPage(tk.Frame):
    def __init__(self, master=None, verification_code=""):
        super().__init__(master)
        self.master = master
        self.pack()

        # Save verification code for later
        self.verification_code = verification_code

        # Create widgets for verification page
        self.verification_label = tk.Label(self, text="Verification Code:")
        self.verification_label.pack()
        self.verification_entry = tk.Entry(self)
        self.verification_entry.pack()

        self.cancel_button = tk.Button(self, text="Cancel", command=self.cancel)
        self.cancel_button.pack()

        self.verify_button = tk.Button(self, text="Verify", command=self.verify)
        self.verify_button.pack()

    def verify(self):
        # Get user-entered verification code
        user_code = self.verification_entry.get()

        # Compare with actual verification code
        if user_code == self.verification_code:
            # Verification successful, return to signup page
            self.pack_forget()
            SignupPage(self.master)
        else:
            # Verification failed, show error message
            self.error_label = tk.Label(self, text="Incorrect verification code")
            self.error_label.pack()

    def cancel(self):
        # Return to signup page
        self.pack_forget()
        SignupPage(self.master)

root = tk.Tk()
app = SignupPage(master=root)
app.mainloop()
