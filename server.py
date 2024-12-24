import socket
from threading import Thread
import time
import os

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

IP_ADDR = '127.0.0.1'
PORT = 5550
SERVER = None
BUFFER_SIZE = 4096

clients={}

is_dir_exists = os.path.isdir("shared_files")
print(is_dir_exists)
if(not is_dir_exists):
    os.makedirs("shared_files")

def handleClient(client,client_name):
    pass

def accept_connection():
    global SERVER
    global clients

    while True:
        client,addr = SERVER.accept()
        client_name = client.recv(4096).decode().lower()
        clients[client_name]= {
            "client" : client,
            "address" : addr,
            "connected_with" : "",
            "file_name" : "",
            "file_size" : 4096
        }

        print(f"Connection established with {client_name}:{addr}")

        thread = Thread(target=handleClient,args=(client,client_name))
        thread.start()

def setup():
    global IP_ADDR
    global PORT
    global SERVER

    SERVER=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    SERVER.bind((IP_ADDR,PORT))
    SERVER.listen(100)

    print("\t\t\t\tSERVER IS WAITING FOR INCOMMING CONNECTIONS...\n")

    accept_connection()

def ftp():
    global IP_ADDR

    dummy = DummyAuthorizer()
    dummy.add_user("lftpd","lftpd",".",perm="elradfmw")

    handler = FTPHandler
    handler.authorizer = dummy

    ftp_server = FTPServer((IP_ADDR,21),handler)
    ftp_server.serve_forever()

setup_thread = Thread(target=setup)
setup_thread.start()

ftp_thread = Thread(target=ftp)
ftp_thread.start()