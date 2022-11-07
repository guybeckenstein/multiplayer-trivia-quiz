# Protocol Constants

CMD_FIELD_LENGTH = 16  # Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4  # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10 ** LENGTH_FIELD_LENGTH - 1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message

# Protocol Messages 
# In this dictionary we will have all the client and server command names

PROTOCOL_CLIENT = {
	"login_msg": "LOGIN",
	"logout_msg": "LOGOUT",
	'logged_msg': "LOGGED",
	'get_question_msg': 'GET_QUESTION',
	'send_answer_msg': 'SEND_ANSWER',
	'my_score_msg': 'MY_SCORE',
	'highscore_msg': 'HIGHSCORE',
	'login_ok_msg': 'LOGIN_OK',
	'logged_answer_msg': 'LOGGED_ANSWER',
	'your_question_msg': 'YOUR_QUESTION',
	'correct_answer_msg': 'CORRECT_ANSWER',
	'wrong_answer_msg': 'WRONG_ANSWER',
	'your_score_msg': 'YOUR_SCORE',
	'all_score_msg': 'ALL_SCORE',
	'error_msg': 'ERROR',
	'no_questions_msg': 'NO_QUESTIONS'
}  # ..  Add more commands if needed

PROTOCOL_SERVER = {
	"login_ok_msg": "LOGIN_OK",
	"login_failed_msg": "ERROR"
}  # ..  Add more commands if needed

# Other constants

ERROR_RETURN = None  # What is returned in case of an error


def build_message(cmd, data):
    """
	Gets command name (str) and data field (str) and creates a valid protocol message
	Returns: str, or None if error occurred
	"""
    # length check
    if (len(cmd) > CMD_FIELD_LENGTH) or (len(data) > MAX_DATA_LENGTH):
        return ERROR_RETURN
    # cmd type check
    if cmd not in PROTOCOL_CLIENT.values():
        return ERROR_RETURN

    full_cmd = cmd
    while len(full_cmd) < CMD_FIELD_LENGTH:
        full_cmd = full_cmd + ' '

    # length part
    full_length = str(len(data))
    while len(full_length) < LENGTH_FIELD_LENGTH:
        full_length = '0' + full_length

    # message part
    full_data = data

    # create full message from all data
    full_msg = full_cmd + DELIMITER + full_length + DELIMITER + full_data
    return full_msg


def parse_message(data):
    """
	Parses protocol message and returns command name and data field
	Returns: cmd (str), data (str). If some error occurred, returns None, None
	"""
    if data == "":
        return ERROR_RETURN, ERROR_RETURN

    full_msg_lst = data.split(DELIMITER)
    if len(full_msg_lst) < 3:
        return ERROR_RETURN, ERROR_RETURN

    cmd, length, msg = full_msg_lst[0], full_msg_lst[1], full_msg_lst[2]
    while ((length != '') and (length != '0')) and ('0' == length[0]):
        length = length[1:]
    length = length.strip()

    if (len(cmd) > CMD_FIELD_LENGTH) or (length.isnumeric() is False) or \
            (len(length) > LENGTH_FIELD_LENGTH) or (len(msg) > MAX_DATA_LENGTH) or (int(length) != len(msg)):
        return ERROR_RETURN, ERROR_RETURN

    # The function should return 2 values
    return cmd.strip(), msg


def split_data(msg, expected_fields):
    """
	Helper method. Gets a string and number of expected fields in it. Splits the string
	using protocol's data field delimiter (|#) and validates that there are correct number of fields.
	Returns: list of fields if all ok. If some error occurred, returns None
	"""
    if (msg.count(DATA_DELIMITER) == expected_fields) and msg != '':
        return msg.split(DATA_DELIMITER)
    else:
        return [ERROR_RETURN]


def join_data(msg_fields):
    """
	Helper method. Gets a list, joins all of its fields to one string divided by the data delimiter.
	Returns: string that looks like cell1#cell2#cell3
	"""
    msg_fields_str = [str(obj) for obj in msg_fields]
    return DATA_DELIMITER.join(msg_fields_str)
