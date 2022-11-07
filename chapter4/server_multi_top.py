import socket
import select

SERVER_IP = "0.0.0.0"
SERVER_PORT = 5555
MAX_MSG_SIZE = 1024


def print_client_sockets(client_sockets):
    for c_s in client_sockets:
        print("\t{data}".format(data=c_s.getpeername()))


def main():
    print("Setting up server...")
    # Create server's socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen()
    print("Listening for clients...")
    client_sockets = []
    while True:
        ready_to_read, ready_to_write, in_error = select.select([server_socket] + client_sockets, [], [])
        for current_socket in ready_to_read:
            if current_socket is server_socket:
                (client_socket, client_address) = current_socket.accept()
                print("New client joined!", client_address)
                client_sockets.append(client_socket)
            else:
                print("New data from client!")
                data = current_socket.recv(MAX_MSG_SIZE).decode()  # Get message from client
                if data == "":
                    print("Connection closed")
                    client_sockets.remove(current_socket)
                    current_socket.close()
                else:
                    print(data)
                    current_socket.send(data.encode())


main()