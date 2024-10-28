import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
import hashlib

class ServerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Server")

        self.master.configure(bg='light yellow')

        font_style = ("Arial", 12)

        self.button_canvas = tk.Canvas(master, width=150, height=40, bg='yellow2', highlightthickness=0, borderwidth=0)
        self.button_canvas.create_text(75, 20, text="Start Server", fill='black', font=font_style)
        self.button_canvas.bind("<Button-1>", self.start_server)  
        self.button_canvas.pack(pady=10)

        self.output_area = scrolledtext.ScrolledText(master, width=50, height=15, font=font_style, bg='white', fg='black')
        self.output_area.pack(pady=10)

        self.server_socket = None
        self.running = False

    def start_server(self, event=None):
        if not self.running:
            self.running = True
            self.output_area.insert(tk.END, "Server is starting...\n")
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind(('localhost', 65432))
            self.server_socket.listen(1)
            threading.Thread(target=self.accept_connections, daemon=True).start()

    def accept_connections(self):
        while self.running:
            self.output_area.insert(tk.END, "Waiting for a connection...\n")
            connection, client_address = self.server_socket.accept()
            self.output_area.insert(tk.END, f"Connection from {client_address}\n")
            threading.Thread(target=self.handle_client, args=(connection,), daemon=True).start()

    def handle_client(self, connection):
        try:
            data = connection.recv(1024)
            if data.decode() == "CONNECT":
                self.output_area.insert(tk.END, "Received connection request from client.\n")
                connection.sendall(b'WHO ARE YOU?') 
                
                credentials = connection.recv(1024).decode()
                username, password = credentials.split(",")

                if self.check_credentials(username, password):
                    connection.sendall(b'Authentication successful!')
                    self.output_area.insert(tk.END, "Client authenticated successfully!\n")
                    self.data_exchange(connection)
                else:
                    connection.sendall(b'Authentication failed, please try again.')
                    self.output_area.insert(tk.END, "Authentication failed.\n")
            else:
                self.output_area.insert(tk.END, "Unexpected message from client.\n")
        finally:
            connection.close()

    def check_credentials(self, username, password):
        stored_username = "Olha_Klishchevska"
        stored_password_hash = hashlib.sha256(b"?client12").hexdigest()
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        return username == stored_username and password_hash == stored_password_hash

    def data_exchange(self, connection):
        while True:
            data = connection.recv(1024)
            if not data:
                break
            self.output_area.insert(tk.END, f"Received: {data.decode()}\n")
            connection.sendall(data)
        self.output_area.insert(tk.END, "Client disconnected.\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = ServerApp(root)
    root.mainloop()
