from common.constants import MAX_MSG_SIZE
from common import chatlib


def build_send_recv_parse(conn, code, data):
    build_and_send_message(conn, code, data)
    return recv_message_and_parse(conn)


def build_and_send_message(conn, code, data):
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    Parameters: conn (socket object), code (str), data (str)
    Returns: Nothing
    """
    full_msg = chatlib.build_message(code, data)
    if full_msg == chatlib.ERROR_RETURN:
        __error_and_exit("ERROR: Failed to build and send message!")
    conn.send(full_msg.encode())


def recv_message_and_parse(conn):
    """
	Receives a new message from given socket,
	then parses the message using chatlib.
	Parameters: conn (socket object)
	Returns: cmd (str) and data (str) of the received message.
	If error occurred, will return None, None
	"""
    full_msg = conn.recv(MAX_MSG_SIZE).decode()

    cmd, data = chatlib.parse_message(full_msg)
    return cmd, data


def __error_and_exit(error_msg):
    raise Exception(error_msg)