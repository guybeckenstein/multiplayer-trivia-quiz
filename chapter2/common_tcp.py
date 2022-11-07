import socket

SERVER_PORT = 8820
MAX_MSG_SIZE = 1024


def initialize_socket(socket_type, **kwargs):
    # we get a socket by this line
    # param socket.AF_INET - meaning that the socket uses IP protocol
    # param socket.SOCK_STREAM - meaning that the socket defines TCP use
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if socket_type == "server":
        # connects between the server socket to all other sockets by adding server's external IP address.
        # Port address is 8820
        my_socket.bind(("0.0.0.0", SERVER_PORT))
        # this line makes this normal 'socket' to an actual server socket
        my_socket.listen()
        print("Server socket is up and running!")
    elif socket_type == "client":
        # connects between the socket to the server by adding server's IP and port addresses
        ip_address = kwargs.get('ip_address', None)
        my_socket.connect((ip_address, SERVER_PORT))
    else:
        raise ValueError('ERROR: Invalid socket type, only \'server\' or \'client\' allowed!')
    return my_socket