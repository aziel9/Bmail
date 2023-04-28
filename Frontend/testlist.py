import tkinter as tk

class MyGUI:
    def __init__(self, master):
        self.master = master
        master.title("Scrollable Text Area")

        self.text = tk.Text(master, wrap="word")
        self.text.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(master, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")

        self.master.after(500, self.update_scrollbar)

    def update_scrollbar(self):
        new_text = self.text.get("1.0", "end-1c")
        if new_text != self.old_text:
            self.old_text = new_text
            self.text.update_idletasks()
            if self.text.winfo_height() >= self.text.winfo_reqheight():
                self.scrollbar.pack_forget()
            else:
                self.scrollbar.pack(side="right", fill="y")
        self.master.after(500, self.update_scrollbar)


    # def hide_scrollbar(self):
    #     self.scrollbar.pack_forget()

    # def show_scrollbar(self):
    #     self.scrollbar.pack(side="right", fill="y")

root = tk.Tk()
gui = MyGUI(root)
root.mainloop()
