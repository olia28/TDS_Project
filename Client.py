import socket
import tkinter as tk
from tkinter import scrolledtext, simpledialog, ttk

class ClientApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Client")
        self.master.configure(bg='azure') 

        style = ttk.Style()
        style.theme_use('clam') 
        style.configure('TButton', font=('Arial', 12, 'bold'), borderwidth=1)
        style.configure('Custom.TButton', background='dodger blue', foreground='white')
        style.map('Custom.TButton', background=[('active', 'deep sky blue')])

        self.connect_button = ttk.Button(master, text="Connect to Server", command=self.start_client, style='Custom.TButton')
        self.connect_button.pack(pady=(20, 10)) 

        self.output_area = scrolledtext.ScrolledText(master, width= 50, height=15, bg='white', fg='black', font=('Arial', 10))
        self.output_area.pack(pady=10)

        self.message_entry = ttk.Entry(master, width=35, font=('Arial', 12))
        self.message_entry.pack(pady=(10, 5))

        self.send_button = ttk.Button(master, text="Send Message", command=self.send_message, style='Custom.TButton')
        self.send_button.pack(pady=10)

        self.client_socket = None

    def start_client(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('localhost', 65432))

        self.client_socket.sendall(b'CONNECT')  
        
        response = self.client_socket.recv(1024).decode()  
        if response == 'WHO ARE YOU?':
            username = simpledialog.askstring("Input", "Enter your username:", parent=self.master)
            password = simpledialog.askstring("Input", "Enter your password:", show='*', parent=self.master)
            credentials = f"{username},{password}"
            self.client_socket.sendall(credentials.encode())

            auth_response = self.client_socket.recv(1024).decode()
            self.output_area.insert(tk.END, f"{auth_response}\n")
            if "successful" in auth_response:
                self.data_exchange()

    def data_exchange(self):
        self.output_area.insert(tk.END, "You can start sending messages:\n")

    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.client_socket.sendall(message.encode())
            response = self.client_socket.recv(1024)
            self.output_area.insert(tk.END, f"Sent: {message}\n")
            self.output_area.insert(tk.END, f"Received from server: {response.decode()}\n")
            self.message_entry.delete(0, tk.END)  

if __name__ == "__main__":
    root = tk.Tk()
    app = ClientApp(root)
    root.mainloop()
