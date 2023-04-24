import socket

from common.constants import MAX_MSG_SIZE
from common import chatlib


def build_send_recv_parse(conn: socket.socket, code: str, data: str) -> tuple[str, str]:
    build_and_send_message(conn, code, data)
    return recv_message_and_parse(conn)


def build_and_send_message(conn: socket.socket, code: str, data: str) -> None:
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    Parameters: conn (socket object), code (str), data (str)
    Returns: Nothing
    """
    full_msg: str = chatlib.build_message(code, data)
    if full_msg == chatlib.ERROR_RETURN:
        __error_and_exit("ERROR: Failed to build and send message!")
    conn.send(full_msg.encode())


def recv_message_and_parse(conn: socket.socket) -> tuple[str, str]:
    """
	Receives a new message from given socket,
	then parses the message using chatlib.
	Parameters: conn (socket object)
	Returns: cmd (str) and data (str) of the received message.
	If error occurred, will return None, None
	"""
    full_msg: str = conn.recv(MAX_MSG_SIZE).decode()

    cmd, data = chatlib.parse_message(full_msg)
    return cmd, data


def __error_and_exit(error_msg: str) -> None:
    raise Exception(error_msg)
