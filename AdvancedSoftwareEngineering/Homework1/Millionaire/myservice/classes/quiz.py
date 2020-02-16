class Answer():
    def __init__(self, answer, correct=False):
        self.answer = answer
        self.correct = correct

    def serialize(self):
        return {'answer': self.answer}


class Question():
    def __init__(self, question, answers):
        self.question = question
        self.answers = answers

    def checkAnswer(self, givenAnswer):
        for answer in self.answers:
            if answer.answer == givenAnswer:
                return answer.correct
        else:
            raise NonExistingAnswerError(givenAnswer)

    def serialize(self):
        return {'question': self.question,
                'answers': [a.serialize() for a in self.answers]}


class Quiz():
    def __init__(self, id, questions):
        self.id = id
        self.questions = questions
        self.currentQuestion = 0

    def checkAnswer(self, givenAnswer):
        self.isOpen()

        question = self.questions[self.currentQuestion]

        if question.checkAnswer(givenAnswer):
            self.currentQuestion += 1
            if self.currentQuestion == len(self.questions):
                self.currentQuestion += 1
                # no more questions, you won the quiz!
                raise CompletedQuizError("You won!")
            return self.currentQuestion  # there are other questions to answer
        else:
            self.currentQuestion = -1
            raise LostQuizError(givenAnswer)  # you lost the quiz!

    def isOpen(self):
        if self.isCompleted():
            raise CompletedQuizError("quiz is completed")
        elif self.isLost():
            raise LostQuizError("quiz is lost")

    def isCompleted(self):
        return self.currentQuestion == len(self.questions) + 1

    def isLost(self):
        return self.currentQuestion == -1

    def getQuestion(self):
        self.isOpen()
        return self.questions[self.currentQuestion].serialize()

    def serialize(self):
        return {'id': self.id,
                'questions': [q.serialize() for q in self.questions]
                }


class NonExistingAnswerError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class LostQuizError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class CompletedQuizError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class WrongAnswerError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
