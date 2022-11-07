import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5555
MAX_MSG_SIZE = 1024


def login():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))
    return client_socket


def main():
    client_socket = login()
    while True:
        msg = input("Please enter your message\n")
        client_socket.send(msg.encode())
        response_msg = client_socket.recv(MAX_MSG_SIZE).decode()
        print("The server sent response: " + response_msg)


main()