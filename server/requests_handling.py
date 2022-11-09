import engine


def send_error(conn, error_msg):
	"""
	Send error message with given message
	Receives: socket, message error string from called function
	Returns: None
	"""
	from engine import chatlib

	code = chatlib.PROTOCOL_SERVER['error_msg']
	engine.build_and_send_message(conn, code, error_msg)
	print("{code}: {info}".format(code=code, info=error_msg))


# MESSAGE HANDLING
def handle_getscore_message(conn, username):
	from engine import chatlib, users

	cmd = chatlib.PROTOCOL_SERVER['your_score_msg']
	data = users[username]["score"]
	engine.build_and_send_message(conn, cmd, str(data))


def handle_question_message(conn):
	from engine import chatlib, logged_users

	cmd = chatlib.PROTOCOL_SERVER['your_question_msg']
	data = engine.create_random_question(logged_users[conn])
	if data is not None:
		engine.build_and_send_message(conn, cmd, data)
	else:
		send_error(conn, "No more questions for {user}!".format(user=logged_users[conn]))


def handle_answer_message(conn, answer):
	from engine import logged_users, chatlib, users

	curr_user = logged_users[conn]
	curr_question = users[curr_user]['questions_asked'][-1]
	correct_answer = curr_question[1][0]
	if answer[-1] == correct_answer:
		cmd = chatlib.PROTOCOL_SERVER['correct_answer_msg']
		data = ""
		users[curr_user]['score'] += 5  # For each correct answer, score is raised by 5
	else:
		cmd = chatlib.PROTOCOL_SERVER['wrong_answer_msg']
		data = str(correct_answer)
		# For each wrong answer, score stays the same
	engine.build_and_send_message(conn, cmd, data)


def handle_highscore_message(conn):
	from engine import chatlib, users

	cmd = chatlib.PROTOCOL_SERVER['all_score_msg']
	data = ""
	high_scores = {}
	for user_score in users.items():
		high_scores[user_score[0]] = user_score[1]['score']
	sorted_high_scores = dict(sorted(high_scores.items(), key=lambda item: item[1], reverse=True))
	first_itr = True
	for score_item in sorted_high_scores.items():
		if first_itr is True:
			data = data + score_item[0] + ': ' + str(score_item[1])
			first_itr = False
		else:
			data = data + '\n' + score_item[0] + ': ' + str(score_item[1])
	engine.build_and_send_message(conn, cmd, data)


def handle_logged_message(conn):
	from engine import chatlib, logged_users

	cmd = chatlib.PROTOCOL_SERVER['logged_answer_msg']
	data = ",".join(logged_users.values())
	engine.build_and_send_message(conn, cmd, data)


def handle_logout_message(conn):
	from engine import chatlib, client_sockets, logged_users

	"""
	Closes the given socket (in later chapters, also remove user from logged_users dictionary)
	Receives: socket
	Returns: None
	"""
	code = chatlib.PROTOCOL_SERVER['logout_msg']
	engine.build_and_send_message(conn, code, "")
	client_sockets.remove(conn)
	if conn in logged_users.keys():
		logged_users.pop(conn)
	conn.close()


def handle_login_message(conn, data):
	from engine import chatlib, users, logged_users

	"""
	Gets socket and message data of login message. Checks if user and pass exists and match.
	If not - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
	Receives: socket, message code and data
	Returns: None (sends answer to client)
	"""

	if data is None:
		send_error(conn, "Invalid message!")
	else:
		username_and_password = chatlib.split_data(data, 1)
		username, password = username_and_password[0], username_and_password[1]
		if (username == "") or (password == ""):
			send_error(conn, "Invalid username or password!")
		elif username not in users.keys():
			send_error(conn, "Username not found!")
		elif users[username]['password'] != password:
			send_error(conn, "Password does not match!")
		elif username in logged_users.values():
			send_error(conn, "User already logged in!")
		else:
			code = chatlib.PROTOCOL_SERVER['login_ok_msg']
			msg = ""
			engine.build_and_send_message(conn, code, msg)
			logged_users[conn] = username


def handle_client_message(conn, cmd, data):
	from engine import logged_users

	"""
	Gets message code and data and calls the right function to handle command
	Receives: socket, message code and data
	Returns: None
	"""
	if conn not in logged_users:
		if cmd == "LOGIN":
			handle_login_message(conn, data)
		else:
			send_error(conn, "Invalid client command!")
	else:
		if cmd == "LOGOUT":
			handle_logout_message(conn)
		elif cmd == "MY_SCORE":
			handle_getscore_message(conn, logged_users[conn])
		elif cmd == "HIGHSCORE":
			handle_highscore_message(conn)
		elif cmd == "GET_QUESTION":
			handle_question_message(conn)
		elif cmd == "SEND_ANSWER":
			handle_answer_message(conn, data)
		elif cmd == "LOGGED":
			handle_logged_message(conn)
		else:
			send_error(conn, "Invalid client command!")