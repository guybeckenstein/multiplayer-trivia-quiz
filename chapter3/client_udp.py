import socket

SERVER_IP = "127.0.0.1"
PORT = 8821
MAX_MSG_SIZE = 1024

my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
input_val = ""
while input_val.upper() != "EXIT":
    input_val = input("Please send message for server: ")
    my_socket.sendto(input_val.encode(), (SERVER_IP, PORT))
    # response - msg, remote_address - IP address of sender
    (response, remote_address) = my_socket.recvfrom(MAX_MSG_SIZE)
    data = response.decode()
    print("The server sent " + data)
# close socket
my_socket.close()