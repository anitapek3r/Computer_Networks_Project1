from tkinter import *
from tkinter import simpledialog
from client import Client

BG_GRAY="#096B68"
BG_COLOR="#EBF4DD"
TEXT_COLOR="#3B4953"

FONT =" Helvetica 14"
FONT_BOLD ="Helvetica 13 bold"

##colors per sender
COLOR_YOU = "#0D4715"      #messages from you
COLOR_SERVER = "#9E3B3B"   #messages from the server
COLOR_OTHER = "#132440"    #messages from other clients

#function to enter user name
def ask_username():
    root = Tk()
    root.withdraw() 
    username = simpledialog.askstring("Username", "Enter your name:")
    root.destroy()
    return username

class ChatApplication: ##opens a dialog window asking the user for a username

    def __init__(self):
        self.window = Tk()
        self.client = None
        self._setup_main_window()

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title("chat")
        self.window.resizable(width=False,height=False)
        self.window.configure(width=470,height=550, bg=BG_COLOR)

        #header label showing active clients
        self.head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR, text="ACTIVE CLIENTS: 0", font=FONT_BOLD, pady=10)
        self.head_label.place(relwidth=1)

        line=Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, rely=0.07, relheight=0.012)

        #text widget
        self.text_widget= Text(self.window, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, padx=5, pady=5, wrap=WORD)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED)
        
        # tags for the colors
        self.text_widget.tag_config("you", foreground=COLOR_YOU, font=FONT_BOLD)
        self.text_widget.tag_config("server", foreground=COLOR_SERVER, font=FONT_BOLD)
        self.text_widget.tag_config("other", foreground=COLOR_OTHER, font=FONT_BOLD)

        #scroll bar
        scrollbar= Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_widget.yview)

        #footer label
        bottom_label = Label(self.window, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.825)

        #message entry box
        self.msg_entry = Entry(bottom_label, bg="#5A7863", font=FONT)
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)

        #target client entry
        Label(bottom_label, text="To:", bg=BG_GRAY, fg="white", font=FONT_BOLD).place(relx=0.52, rely=0.1)
        self.target_entry = Entry(bottom_label, bg="#5A7863", font=FONT)
        self.target_entry.place(relwidth=0.25, relheight=0.06, relx=0.57, rely=0.1)

        #send button
        send_button = Button(bottom_label, text="Send", font=FONT_BOLD, width=20, bg=BG_GRAY, command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.77, rely=0.008, relheight=0.06,relwidth=0.27)

        #auto connection
        self._connect_client()

    def _connect_client(self):
        username = ask_username()
        if not username:
            self._insert_message("No username provided. Connection cancelled.", "Server")
            return
    
        self.client = Client(username, self._receive_message, self._update_active_clients)
        result = self.client.connect()
        self._insert_message(result, "Server")

    def _update_active_clients(self, client_list):
        count = len(client_list)
        clients_text = ", ".join(client_list)if client_list else "None"
        
        def update():
            self.head_label.config(text=f"Active clients ({count}): {clients_text}")
        
        self.window.after(0, update)

    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get().strip()
      
        if not msg:
            return
        
        self._insert_message(msg, "You")

        if self.client:
            self.client.send_message(msg)

        self.msg_entry.delete(0, END)
    
    def _insert_message(self, msg, sender):
        if not msg:
            return
        
        self.text_widget.configure(state=NORMAL)
        
        ##color based on who sent the message
        if sender == "You":
            tag = "you"
            sender_text = f"{sender}: "
        elif sender == "Server":
            tag = "server"
            sender_text = f"{sender}: "
        elif sender:  ## message from another client
            tag = "other"
            sender_text = f"{sender}: "
        else:
            tag = "other"
            sender_text = ""
        
        if sender_text:
            self.text_widget.insert(END, sender_text, tag)
        
        self.text_widget.insert(END, f"{msg}\n\n")
        
        self.text_widget.configure(state=DISABLED)
        self.text_widget.see("end")

    def _receive_message(self, msg):
        if msg.startswith("From "):
            sender_name = msg[5:msg.index(":")]
            self.window.after(0, self._insert_message, msg[msg.index(":")+2:], f"From {sender_name}")
        else:
            self.window.after(0, self._insert_message, msg, "Server")
      

if __name__ == "__main__":
    app=ChatApplication()
    app.run()