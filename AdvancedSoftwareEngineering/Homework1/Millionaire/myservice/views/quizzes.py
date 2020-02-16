from flakon import JsonBlueprint
from flask import request, jsonify, abort
from myservice.classes.quiz import Quiz, Question, Answer, NonExistingAnswerError, LostQuizError, CompletedQuizError

quizzes = JsonBlueprint('quizzes', __name__)

_LOADED_QUIZZES = {}  # list of available quizzes
_QUIZNUMBER = 0  # index of the last created quizzes


@quizzes.route("/quizzes", methods=['GET', 'POST'])
def all_quizzes():
    if 'POST' == request.method:
        # Create new quiz
        result = create_quiz(request)
    elif 'GET' == request.method:
        # Retrieve all loaded quizzes
        result = get_all_quizzes(request)

    return result


@quizzes.route("/quizzes/loaded", methods=['GET'])
def loaded_quizzes():
    # returns the number of quizzes currently loaded in the system
    result = len(_LOADED_QUIZZES)

    return jsonify({'loaded_quizzes': result})


@quizzes.route("/quiz/<id>", methods=['GET', 'DELETE'])
def single_quiz(id):
    global _LOADED_QUIZZES
    result = ""

    # Checking that the quiz exists
    exists_quiz(id)

    if 'GET' == request.method:
        # retrieve a quiz <id>
        result = _LOADED_QUIZZES[id].serialize()

    elif 'DELETE' == request.method:
        # delete a quiz and get back number of answered questions
        # and total number of questions
        num = len(_LOADED_QUIZZES)
        answ_quest = _LOADED_QUIZZES[id].currentQuestion
        result = jsonify({'answered_questions': answ_quest, 'total_questions': num})
        _LOADED_QUIZZES.pop(id)

    return result


@quizzes.route("/quiz/<id>/question", methods=['GET'])
def play_quiz(id):
    global _LOADED_QUIZZES
    result = ""

    # check if the quiz is an existing one
    exists_quiz(id)
    pointer = _LOADED_QUIZZES[id]

    if 'GET' == request.method:
        # retrieve next question in a quiz, handle exceptions
        try:
            result = pointer.getQuestion()
        except CompletedQuizError:
            result = jsonify({'msg': 'completed quiz'})
        except LostQuizError:
            result = jsonify({'msg': 'you lost!'})

    return result


@quizzes.route("/quiz/<id>/question/<answer>", methods=['PUT'])
def answer_question(id, answer):
    global _LOADED_QUIZZES
    result = ""

    # check if the quiz is an existing one
    exists_quiz(id)
    quiz = _LOADED_QUIZZES[id]

    # check if quiz is lost or completed and act consequently

    try:
        quiz.isLost()
    except LostQuizError:
        return jsonify({'msg': 'you lost!'})

    if quiz.isCompleted():
        return jsonify({'msg': 'completed quiz'})

    if 'PUT' == request.method:
        # Check answers and handle exceptions
        try:
            result = jsonify({'msg': quiz.checkAnswer(answer)})
        except CompletedQuizError:
            result = jsonify({'msg': 'you won 1 million clams!'})
        except LostQuizError:
            result = jsonify({'msg': 'you lost!'})
        except NonExistingAnswerError:
            result = jsonify({'msg': 'non-existing answer!'})

    return result


############################################
# USEFUL FUNCTIONS BELOW (use them, don't change them)
############################################

def create_quiz(request):
    global _LOADED_QUIZZES, _QUIZNUMBER

    json_data = request.get_json()
    qs = json_data['questions']
    questions = []
    for q in qs:
        question = q['question']
        answers = []
        for a in q['answers']:
            answers.append(Answer(a['answer'], a['correct']))
        question = Question(question, answers)
        questions.append(question)

    _LOADED_QUIZZES[str(_QUIZNUMBER)] = Quiz(_QUIZNUMBER, questions)
    _QUIZNUMBER += 1

    return jsonify({'quiznumber': _QUIZNUMBER - 1})


def get_all_quizzes(request):
    global _LOADED_QUIZZES

    return jsonify(loadedquizzes=[e.serialize() for e in _LOADED_QUIZZES.values()])


def exists_quiz(id):
    if int(id) > _QUIZNUMBER:
        abort(404)  # error 404: Not Found, i.e. wrong URL, resource does not exist
    elif not (id in _LOADED_QUIZZES):
        abort(410)  # error 410: Gone, i.e. it existed but it's not there anymore
