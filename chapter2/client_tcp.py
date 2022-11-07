from common_tcp import initialize_socket, MAX_MSG_SIZE

SERVER_IP = "127.0.0.1"


def send_message_to_server_and_print_server_response(my_socket, msg):
    # sends message to the server. message must be binary, so we must encode it
    my_socket.send(msg.encode())

    # returned message given by server.
    # 1024 is the maximum number of bytes we are using for decode (up to 1024).
    # Message must be text, so we must decode it from binary.
    response_msg = my_socket.recv(MAX_MSG_SIZE).decode()
    print("The server sent response: " + response_msg)
    return response_msg


def socket_test():
    my_socket = initialize_socket('client', ip_address=SERVER_IP)

    msg = ""
    while msg.upper() != "BYE":
        msg = input("Please enter your message\n")
        msg = send_message_to_server_and_print_server_response(my_socket, msg)

    # closes the socket
    my_socket.close()


socket_test()

# def message_format():
#     pass
