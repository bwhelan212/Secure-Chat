'''
import socket
import os
import sys
from server_commands import accout_option
#from server_commands import command_handler

def server_handler (client_socket):
    welcome_msg = "\n-------WELCOME TO SECURE CHAT-------\n\n"
    client_socket.send(welcome_msg.encode())


    options_msg = "Press 1 to create an account, 2 to log into an existing account, or 3 to quit: "
    client_socket.send(options_msg.encode())
    print("meow1")

    while(True):

        print("meow1.5")
        
        #get user command
        client_command = client_socket.recv(1024)
        print("meow2")

        #if user disconnects
        if not client_command:
            print("Client disconnected.")
            return
        
        #print what command client sent
        print ("client send " + str(client_command.decode()) + ".")

        #handle account option
        response = accout_option(client_command, client_socket)

        #handle the client command
        #response = command_handler(client_command, client_socket)

        #if response is in bytes just send it
        #if isinstance(response, bytes):
            #client_socket.send(response)
        #else:
            #otherwise encode it
            #client_socket.send(response.encode())


def start_server(port):
    #server IP
    server_ip = "127.0.0.1"
    #create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #associate the socket with the port
    server_socket.bind((server_ip, port))

    #start a listening for incoming connections (we can have # connection in queue before reject new connections
    server_socket.listen(1)

    while(True):
        print ("Waiting for clients to connect...")

        #Accept a waiting connection
        client_socket, client_info = server_socket.accept()

        print ("Client connected from: " + str(client_info))

        server_handler(client_socket)


if __name__ == "__main__":
    #check if a port number is provided as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python3 server.py <port>")
        sys.exit(1)

    try:
        #convert the provided argument to an integer (the port number)
        port = int(sys.argv[1])
    except ValueError:
        print("Invalid port number. Please provide a valid integer.")
        sys.exit(1)

    start_server(port)'''


import socket
import os
import sys
from server_commands import accout_option
from server_commands import command_handler
import threading

clients = []
# usernames = []
def server_handler (client_socket):
    welcome_msg = "----You have successfully connected to Secure Chat!----\n\n"
    client_socket.send(welcome_msg.encode())
    while(True):

        options_msg = "Press 1 to create an account, 2 to log into an existing account, or 3 to quit: \n"
        client_socket.send(options_msg.encode())

        #get user command
        client_command = client_socket.recv(1024)

        print(client_command)

        #if user disconnects
        if not client_command:
            print("Client disconnected.")
            return
        
        #print what command client sent
        print ("client send " + str(client_command.decode()) + ".")

        accout_option(client_command, client_socket)
        command_handler(client_socket)

              #connection_socket.send(("Welcome " + username + "!").encode())


def start_server(port):
    #reset online.txt whenever server.py ran
    f = open("online.txt", "w")
    f.close()
    #server IP
    server_ip = "127.0.0.1"
    #create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #associate the socket with the port
    server_socket.bind((server_ip, port))

    #start a listening for incoming connections (we can have # connection in queue before reject new connections
    server_socket.listen(2)

    while(True):
        print ("Waiting for clients to connect...")

        #Accept a waiting connection
        client_socket, client_info = server_socket.accept()

        print ("Client connected from: " + str(client_info))
        clients.append(client_socket)
        
        #server_handler(client_socket)
        #thread so client can send messages to server
        thread = threading.Thread(target=server_handler, args=(client_socket,))
        thread.start()


if __name__ == "__main__":
    #check if a port number is provided as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python3 server.py <port>")
        sys.exit(1)

    try:
        #convert the provided argument to an integer (the port number)
        port = int(sys.argv[1])
    except ValueError:
        print("Invalid port number. Please provide a valid integer.")
        sys.exit(1)

    start_server(port)