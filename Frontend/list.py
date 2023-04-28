import tkinter as tk
import psycopg2

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    database="emailapp",
    user="postgres",
    password="apeed",
    host="localhost"
)

def get_messages():
    cur = conn.cursor()
    data = """SELECT *FROM messages where receiver='dip@login.com' ORDER BY time DESC"""
    cur.execute(data)
    messages = cur.fetchall()
    cur.close()
    return messages

def update_listbox():
    messages = get_messages()
    print(messages)
    listbox.delete(0, tk.END)
    for message in messages:
        listbox.insert(tk.END, f"{message[1]}")

# Define the function to display a message when it is selected in the listbox
def show_message(event):
    selection=event.widget.curselection()
    if selection:
        index = selection[0]
        messages = get_messages()
        message = messages[index]

        # Display the message details in the text widget
        text.delete("1.0", tk.END)
        text.insert(tk.END, f"Sender:{message[1]} \n\nReceiver={message[2]} \n\nDate:{message[0]} \n\nSubject:{message[3]} \n\n{message[4]}")

# Create the main window
root = tk.Tk()
root.geometry("800x600")
root.title("Inbox")

# Create a frame for the listbox on the left side of the window
listbox_frame = tk.Frame(root, width=400, height=600)
listbox_frame.pack(side="left", fill="y")

# Create the listbox
listbox = tk.Listbox(listbox_frame, width=50, height=10)
listbox.bind("<<ListboxSelect>>", show_message)
listbox.pack(side="left", fill="both", expand=True)

# Create a vertical scrollbar for the listbox
scrollbar = tk.Scrollbar(listbox_frame, orient="vertical", command=listbox.yview)
scrollbar.pack(side="right", fill="y")
listbox.configure(yscrollcommand=scrollbar.set)

# Load the inbox
update_listbox()

# Create a frame for the text widget on the right side of the window
text_frame = tk.Frame(root, width=400, height=600)
text_frame.pack(side="right", fill="y")

# Create the text widget
text = tk.Text(text_frame)
text.pack(side="left", fill="both", expand=True)

# Start the main loop
root.mainloop()
