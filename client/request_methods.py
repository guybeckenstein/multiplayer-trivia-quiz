from engine import *


def get_score(conn: socket.socket) -> None:
    code: str = "MY_SCORE"
    data: str = ""
    _, data = build_send_recv_parse(conn, code, data)
    print("Your score is " + data)


def get_highscore(conn: socket.socket) -> None:
    code: str = "HIGHSCORE"
    data: str = ""
    _, data = build_send_recv_parse(conn, code, data)
    print("High-Score table:")
    print(data)


def play_question(conn: socket.socket) -> None:
    # Get question from server
    code: str = "GET_QUESTION"
    data: str = ""
    _, data = build_send_recv_parse(conn, code, data)
    # Print question to client
    data_list: list = chatlib.split_data(data, 5)
    if data_list[0] is not None:
        question_id = data_list[0]
        print("Q: {question}:".format(question=data_list[1]))
        for answer_idx in range(1, 5):
            print("\t{answer_id}. {answer_val}".format(answer_id=answer_idx, answer_val=data_list[1 + answer_idx]))
        # Answer question
        answer = __get_question_answer()
        code = "SEND_ANSWER"
        data = chatlib.join_data([question_id, answer])
        response, data = build_send_recv_parse(conn, code, data)
        if response == 'WRONG_ANSWER':
            print('Nope, correct answer is #' + data)
        else:
            print('YES!!!!')
    else:
        print("{error}: {reason}".format(error=_, reason=data))


def __get_question_answer() -> int:
    answer = None
    valid_answer_value: bool = False
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


def get_logged_users(conn: socket.socket) -> None:
    code: str = "LOGGED"
    data: str = ""
    _, data = build_send_recv_parse(conn, code, data)
    print('Logged users:\n{data}'.format(data=data))
