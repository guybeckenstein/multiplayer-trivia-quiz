import html


def fix_new_question_answers_string(new_question_answers):
	fixed_new_question_answers = []
	for question_answer in new_question_answers:
		fixed_question_answer = html.unescape(question_answer)
		fixed_question_answer = fixed_question_answer.encode().decode('unicode-escape')
		fixed_new_question_answers.append(fixed_question_answer)
	return fixed_new_question_answers


def fix_new_question_string(question):
	fixed_question = html.unescape(question['question'])
	fixed_question = fixed_question.encode().decode('unicode-escape')
	return fixed_question