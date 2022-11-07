import socket
import chatlib

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678
MAX_BYTE_SIZE = 1024


# MAIN SOCKET METHODS
def build_send_recv_parse(conn, code, data):
    build_and_send_message(conn, code, data)
    return recv_message_and_parse(conn)


def get_score(conn):
    code = "MY_SCORE"
    data = ""
    _, data = build_send_recv_parse(conn, code, data)
    print("Your score is " + data)


def get_highscore(conn):
    code = "HIGHSCORE"
    data = ""
    _, data = build_send_recv_parse(conn, code, data)
    print("High-Score table:")
    print(data)


def play_question(conn):
    # Get question from server
    code = "GET_QUESTION"
    data = ""
    _, data = build_send_recv_parse(conn, code, data)
    # Print question to client
    data_list = chatlib.split_data(data, 5)
    question_id = data_list[0]
    print("Q: {question}:".format(question=data_list[1]))
    for answer_id in range(1, 5):
        print("\t{answer_id}. {answer_val}".format(answer_id=answer_id, answer_val=data_list[1 + answer_id]))
    # Answer question
    answer = get_question_answer()
    code = "SEND_ANSWER"
    data = chatlib.join_data([question_id, answer])
    response, data = build_send_recv_parse(conn, code, data)
    if response == 'WRONG_ANSWER':
        print('Nope, correct answer is #' + data)
    else:
        print('YES!!!!')


def get_question_answer():
    answer = None
    valid_answer_value = False
    while valid_answer_value is False:
        answer = input("Please choose an answer [1-4]: ")
        try:
            answer = int(answer)
            if (answer > 4) or (answer < 1):
                print('ERROR: Please choose valid answer [1-4]!')
            else:
                valid_answer_value = True
        except ValueError:
            print('ERROR: Please enter an integer answer!')
    return answer


def get_logged_users(conn):
    code = "LOGGED"
    data = ""
    _, data = build_send_recv_parse(conn, code, data)
    print('Logged users:\n{data}'.format(data=data))


# HELPER SOCKET METHODS
def build_and_send_message(conn, code, data):
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    Parameters: conn (socket object), code (str), data (str)
    Returns: Nothing
    """
    full_msg = chatlib.build_message(code, data)
    if full_msg == chatlib.ERROR_RETURN:
        error_and_exit("ERROR: Failed to build and send message!")
    conn.send(full_msg.encode())


def recv_message_and_parse(conn):
    """
	Receives a new message from given socket,
	then parses the message using chatlib.
	Parameters: conn (socket object)
	Returns: cmd (str) and data (str) of the received message.
	If error occurred, will return None, None
	"""
    full_msg = conn.recv(MAX_BYTE_SIZE).decode()

    cmd, data = chatlib.parse_message(full_msg)
    return cmd, data


def connect():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((SERVER_IP, SERVER_PORT))
    return my_socket


def error_and_exit(error_msg):
    raise Exception(error_msg)


def get_username():
    username = ""
    first_itr = True
    while username == "":
        if first_itr is False:
            print("ERROR: You have not entered an username!")
        else:
            first_itr = True
        username = input("Please enter username: ")
    return username


def get_password():
    password = ""
    first_itr = True
    while password == "":
        if first_itr is False:
            print("ERROR: You have not entered a password!")
        else:
            first_itr = True
        password = input("Please enter password: ")
    return password


def login(conn):
    print("Connecting to " + SERVER_IP + " port " + str(SERVER_PORT))
    valid_login = False
    while valid_login is False:
        # Input
        username = get_username()
        password = get_password()
        data = chatlib.join_data([username, password])  # Helper method that separates username from password within '#'

        # Send message to server
        build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["login_msg"], data)

        # Get response message from server
        cmd, data = recv_message_and_parse(conn)
        if (cmd != chatlib.ERROR_RETURN) and (data != chatlib.ERROR_RETURN):
            print("Logged in!")
            valid_login = True
        else:
            print("ERROR: Failed to login!")


def logout(conn):
    build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["logout_msg"], "")
    print("Goodbye!")
    conn.close()


def main():
    client_socket = connect()
    login(client_socket)
    choice = ""
    while choice.upper() != "Q":
        print("p\tPlay a trivia question")
        print("s\tGet my score")
        print("h\tGet high score")
        print("l\tGet logged users")
        print("q\tQuit")
        choice = input("Please enter your choice: ")
        if choice.upper() == "P":
            play_question(client_socket)
        elif choice.upper() == "S":
            get_score(client_socket)
        elif choice.upper() == "H":
            get_highscore(client_socket)
        elif choice.upper() == "L":
            get_logged_users(client_socket)
    logout(client_socket)


if __name__ == '__main__':
    main()
