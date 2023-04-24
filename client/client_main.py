import socket
import request_methods
import engine

from common.constants import SERVER_PORT, SERVER_IP
from common import chatlib


def __connect() -> socket.socket:
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((SERVER_IP, SERVER_PORT))
    return my_socket


def __get_username() -> str:
    username = ""
    first_itr = True
    while username == "":
        if first_itr is False:
            print("ERROR: You have not entered an username!")
        else:
            first_itr = True
        username = input("Please enter username: ")
    return username


def __get_password() -> str:
    password = ""
    first_itr = True
    while password == "":
        if first_itr is False:
            print("ERROR: You have not entered a password!")
        else:
            first_itr = True
        password = input("Please enter password: ")
    return password


def __login(conn) -> None:
    print("Connecting to " + SERVER_IP + " port " + str(SERVER_PORT))
    valid_login: bool = False
    while valid_login is False:
        # Input
        username: str = __get_username()
        password: str = __get_password()
        # Helper method ('join_data') that separates username from password within '#'
        data: str = chatlib.join_data([username, password])

        # Send message to server
        engine.build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["login_msg"], data)

        # Get response message from server
        cmd, data = engine.recv_message_and_parse(conn)
        if (cmd != chatlib.ERROR_RETURN) and (data != chatlib.ERROR_RETURN) and (cmd != 'ERROR'):
            print("Logged in!")
            valid_login = True
        else:
            print("ERROR: " + data)


def __logout(conn):
    engine.build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["logout_msg"], "")
    print("Goodbye!")
    conn.close()


def main():
    client_socket = __connect()
    __login(client_socket)
    choice = ""
    while choice.upper() != "Q":
        print("p\tPlay a trivia question")
        print("s\tGet my score")
        print("h\tGet high score")
        print("l\tGet logged users")
        print("q\tQuit")
        choice = input("Please enter your choice: ")
        if choice.upper() == "P":
            request_methods.play_question(client_socket)
        elif choice.upper() == "S":
            request_methods.get_score(client_socket)
        elif choice.upper() == "H":
            request_methods.get_highscore(client_socket)
        elif choice.upper() == "L":
            request_methods.get_logged_users(client_socket)
    __logout(client_socket)


if __name__ == '__main__':
    main()
