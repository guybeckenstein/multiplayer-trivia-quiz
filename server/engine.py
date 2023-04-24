import json
import random
import socket

import requests

from common.constants import MAX_MSG_SIZE
from common import chatlib
from server import html_parser

# GLOBALS
users: dict = {}  # {username: {"password": password, "score": score, "questions_asked": questions_asked}}
questions: dict = {}  # {question_id: [original question, answer1, answer2, answer3, answer4]}
logged_users: dict = {}  # a dictionary of client hostnames to usernames - will be used later
client_sockets: list = []  # list of client sockets
messages_to_send: list = []  # list of tuples(socket, string of message to send)


# Main methods for requests & responses
def build_and_send_message(conn: socket.socket, code: str, msg: str) -> None:
	"""
	Builds a new message using chatlib, wanted code and message.
	Prints debug info, then sends it to the given socket.
	Parameters: conn (socket object), code (str), data (str)
	Returns: Nothing
	"""
	global messages_to_send
	full_msg: str = chatlib.build_message(code, msg)
	if full_msg == chatlib.ERROR_RETURN:
		raise Exception("ERROR: Failed to build and send message!")
	elif code != chatlib.PROTOCOL_SERVER['logout_msg']:
		messages_to_send.append((conn, full_msg))
	print("[SERVER] ", full_msg)  # Debug print


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
	print("[CLIENT] ", full_msg)  # Debug print
	return cmd, data


# SERVER ENGINE FUNCTIONS
def create_random_question(username: str) -> str:
	global questions
	curr_user_questions_asked_set: set = {key for key, value in set(users[username]['questions_asked'])}
	questions_list: list = sorted(list(set(questions.keys()) - curr_user_questions_asked_set))
	size: int = len(questions_list)
	if size > 0:
		random_question_idx = random.randrange(len(questions_list))
		question = questions_list[random_question_idx]
		question_key = questions[question]['question']
		question_value = questions[question]['answers']
		question_answer = questions[question]['correct']
		values_to_send = [question_answer, question_key, question_value[0], question_value[1],
						  question_value[2], question_value[3]]
		question_format: str = chatlib.join_data(values_to_send)
		users[username]['questions_asked'].append((questions_list[random_question_idx], question_format))
		return question_format
	else:  # No more questions
		return None


# Main methods for database
def load_user_database() -> None:
	"""
	Loads users list from JSON file
	Receives: -
	Returns: user dictionary
	"""
	global users
	# Loads all users from database into 'users' variable
	with open("../database/users.json") as users_json:
		users = json.load(users_json)


def __get_correct_answer_idx(new_question_answers, question) -> int:
	idx_of_correct_answer = 1
	for answer in new_question_answers:
		if answer == question['correct_answer']:
			break
		idx_of_correct_answer += 1
	return idx_of_correct_answer


def load_questions_from_web() -> None:
	"""
	Loads questions bank from web
	Receives: -
	Returns: questions dictionary
	"""
	global questions
	# Loads random web questions into our 'questions' variable
	response = requests.get(url="https://opentdb.com/api.php?amount=50&type=multiple")
	if response.status_code == 200:
		body: str = response.text
		# Load JSON
		deserialized_value = json.loads(body)
		all_questions = deserialized_value['results']
		for idx, question in enumerate(all_questions):
			new_question_answers = question['incorrect_answers'] + [question['correct_answer']]
			random.shuffle(new_question_answers)
			# Get correct answer index
			idx_of_correct_answer = __get_correct_answer_idx(new_question_answers, question)
			# Fix question answers
			fixed_new_question_answers = html_parser.fix_new_question_answers_string(new_question_answers)
			fixed_new_question = html_parser.fix_new_question_string(question)

			new_question_dict: dict = {
				'question': fixed_new_question,
				'answers': fixed_new_question_answers,
				'correct': idx_of_correct_answer
			}

			questions[idx + 1] = new_question_dict
	else:
		raise ConnectionError("Invalid response status code, got {status_code}!".format(status_code=response.status_code))


# RELEVANT FOR QUESTIONS FROM EXISTING DATABASE, BUT CURRENTLY THIS CODE USES RANDOM QUESTIONS FROM WEB SCRAPING
'''
def load_questions():
	"""
	Loads questions bank from JSON file
	Receives: -
	Returns: questions dictionary
	"""
	global questions
	# Loads all questions from database into 'questions' variable
	with open("../database/questions.json") as question_json:
		questions = json.load(question_json)
	return questions
'''
