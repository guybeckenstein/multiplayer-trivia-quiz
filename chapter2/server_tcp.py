from common_tcp import initialize_socket, MAX_MSG_SIZE


def close_all_sockets():
    # closes client's socket
    client_socket.close()
    # closes server's socket
    server_socket.close()


server_socket = initialize_socket('server')

# this code is being run only after a client request is being given
# param client_socket - all related information of client
# param client_address - client's IP and port addresses
(client_socket, client_address) = server_socket.accept()
print("Client connected!")

while True:
    # reads data given from client's socket. Decodes it, so we can see it as text and not binary
    msg = client_socket.recv(MAX_MSG_SIZE).decode()
    print('Client sent: ' + msg)
    if msg.upper() == "QUIT":
        # closes server side, then client side
        print("Closing client socket now...")
        client_socket.send("Bye".encode())
        break
    else:
        # returns the client's socket input as output
        client_socket.send(msg.encode())

close_all_sockets()