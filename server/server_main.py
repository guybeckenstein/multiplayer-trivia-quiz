import socket
import select

from common.constants import SERVER_IP, SERVER_PORT
import engine
import requests_handling


# SOCKET CREATOR
def __setup_socket():
	"""
	Creates new listening socket and returns it
	Receives: -
	Returns: the socket object
	"""
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind((SERVER_IP, SERVER_PORT))
	server_socket.listen()
	return server_socket


def main():
	from engine import load_user_database, load_questions_from_web, client_sockets, chatlib, messages_to_send

	# Initializes the global users and questions dictionaries using load functions, will be used later
	load_user_database()
	load_questions_from_web()
	print("Welcome to Trivia Server!")
	# initialize server socket
	server_socket = __setup_socket()
	# Wait for new sockets or new messages from existing sockets
	while True:
		ready_to_read, ready_to_write, _ = select.select([server_socket] + client_sockets, client_sockets, [])
		for current_socket in ready_to_read:
			# Add new socket
			if current_socket is server_socket:
				(client_socket, client_address) = current_socket.accept()
				client_sockets.append(client_socket)
				print("New client joined! " + str(client_socket.getpeername()))
			else:
				# Get info from new socket
				cmd, data = engine.recv_message_and_parse(current_socket)
				if (cmd is None) or (cmd == "") or (cmd == chatlib.PROTOCOL_CLIENT["logout_msg"]):
					print("Failed to connect {client}, connection closed.".format(
						client=str(current_socket.getpeername())))
					requests_handling.handle_logout_message(current_socket)
				else:
					print("Received {client} message.".format(client=str(current_socket.getpeername())))
					requests_handling.handle_client_message(current_socket, cmd, data)
		# Send all messages to original client sender, then delete them
		for current_socket, data in messages_to_send:
			if current_socket in ready_to_write:
				current_socket.send(data.encode())
				messages_to_send.remove((current_socket, data))


if __name__ == '__main__':
	main()
