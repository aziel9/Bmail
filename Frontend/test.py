import tkinter as tk

class ButtonMenu:
    def __init__(self, master):
        self.master = master
        master.title("Button Menu")

        # Create the left-side panel of buttons
        self.button_frame = tk.Frame(master, padx=10, pady=10)
        self.button_frame.pack(side=tk.LEFT)

        self.button1 = tk.Button(self.button_frame, text="Button 1", command=lambda: self.change_color(self.button1))
        self.button1.pack(fill=tk.X)

        self.button2 = tk.Button(self.button_frame, text="Button 2", command=lambda: self.change_color(self.button2))
        self.button2.pack(fill=tk.X)

        self.button3 = tk.Button(self.button_frame, text="Button 3", command=lambda: self.change_color(self.button3))
        self.button3.pack(fill=tk.X)

        # Create the right-side frame for displaying clicked button text
        self.display_frame = tk.Frame(master, padx=10, pady=10)
        self.display_frame.pack(side=tk.RIGHT)

        self.clicked_label = tk.Label(self.display_frame, text="Click a button!")
        self.clicked_label.pack()

        # Keep track of the last clicked button
        self.last_clicked = None

    def change_color(self, button):
        # Change the color of the clicked button
        button.configure(bg="red")
        self.clicked_label.configure(text=button.cget("text"))

        # Change the color of the last clicked button back to normal
        if self.last_clicked is not None and self.last_clicked != button:
            self.last_clicked.configure(bg=self.master.cget("bg"))

        # Update the last clicked button
        self.last_clicked = button

root = tk.Tk()
menu = ButtonMenu(root)
root.mainloop()
