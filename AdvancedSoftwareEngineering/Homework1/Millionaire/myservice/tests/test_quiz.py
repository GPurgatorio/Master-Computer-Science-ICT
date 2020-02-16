import unittest
import json
from flask import request, jsonify
from myservice.app import app as tested_app


class TestApp(unittest.TestCase):

    def test1(self):  # allpolls
        app = tested_app.test_client()

        # no loaded quiz
        reply = app.get('/quizzes/loaded')
        body = json.loads(str(reply.data, 'utf8'))
        self.assertEqual(body['loaded_quizzes'], 0)

        # create 3 quizzes
        reply = app.post('/quizzes',
                         data=json.dumps({
                             "questions": [
                                 {
                                     "question": "What's the answer to all questions?",
                                     "answers": [
                                         {
                                             "answer": "33",
                                             "correct": 0
                                         },
                                         {
                                             "answer": "42",
                                             "correct": 1
                                         },
                                         {
                                             "answer": "1",
                                             "correct": 0
                                         }
                                     ]
                                 },
                                 {
                                     "question": "What's the answer to all questions?",
                                     "answers": [
                                         {
                                             "answer": "33",
                                             "correct": 0
                                         },
                                         {
                                             "answer": "42",
                                             "correct": 1
                                         },
                                         {
                                             "answer": "1",
                                             "correct": 0
                                         }
                                     ]
                                 }
                             ]
                         }),
                         content_type='application/json')

        body = json.loads(str(reply.data, 'utf8'))

        self.assertEqual(body['quiznumber'], 0)

        reply = app.post('/quizzes',
                         data=json.dumps({
                             "questions": [
                                 {
                                     "question": "Who's Wilma's husband?",
                                     "answers": [
                                         {
                                             "answer": "Fred",
                                             "correct": 1
                                         },
                                         {
                                             "answer": "Barney",
                                             "correct": 0
                                         },
                                         {
                                             "answer": "Dyno",
                                             "correct": 0
                                         }
                                     ]
                                 },
                                 {
                                     "question": "Who's Fred's daughter?",
                                     "answers": [
                                         {
                                             "answer": "Wilma",
                                             "correct": 0
                                         },
                                         {
                                             "answer": "Pebbles",
                                             "correct": 1
                                         },
                                         {
                                             "answer": "Betty",
                                             "correct": 0
                                         }
                                     ]
                                 },
                                 {
                                     "question": "Who's Flintstones' pet?",
                                     "answers": [
                                         {
                                             "answer": "Dyno",
                                             "correct": 1
                                         },
                                         {
                                             "answer": "Brontosaure",
                                             "correct": 0
                                         },
                                         {
                                             "answer": "BamBam",
                                             "correct": 0
                                         }
                                     ]
                                 }
                             ]
                         }),
                         content_type='application/json')

        body = json.loads(str(reply.data, 'utf8'))

        self.assertEqual(body['quiznumber'], 1)

        reply = app.post('/quizzes',
                         data=json.dumps({
                             "questions": [
                                 {
                                     "question": "Who's Wilma's husband?",
                                     "answers": [
                                         {
                                             "answer": "Fred",
                                             "correct": 1
                                         },
                                         {
                                             "answer": "Barney",
                                             "correct": 0
                                         },
                                         {
                                             "answer": "Dyno",
                                             "correct": 0
                                         }
                                     ]
                                 },
                                 {
                                     "question": "Who's Fred's daughter?",
                                     "answers": [
                                         {
                                             "answer": "Wilma",
                                             "correct": 0
                                         },
                                         {
                                             "answer": "Pebbles",
                                             "correct": 1
                                         },
                                         {
                                             "answer": "Betty",
                                             "correct": 0
                                         }
                                     ]
                                 },
                                 {
                                     "question": "Who's Flintstones' pet?",
                                     "answers": [
                                         {
                                             "answer": "Dyno",
                                             "correct": 1
                                         },
                                         {
                                             "answer": "Brontosaure",
                                             "correct": 0
                                         },
                                         {
                                             "answer": "BamBam",
                                             "correct": 0
                                         }
                                     ]
                                 }
                             ]
                         }),
                         content_type='application/json')

        body = json.loads(str(reply.data, 'utf8'))

        self.assertEqual(body['quiznumber'], 2)

        # get the three quizzes
        reply = app.get('/quizzes/loaded')
        body = json.loads(str(reply.data, 'utf8'))
        self.assertEqual(body['loaded_quizzes'], 3)

        # get the three quizzes
        reply = app.get('/quizzes')
        body = json.loads(str(reply.data, 'utf8'))

        self.assertEqual(body, {
            "loadedquizzes": [
                {
                    "id": 0,
                    "questions": [
                        {
                            "answers": [
                                {
                                    "answer": "33"
                                },
                                {
                                    "answer": "42"
                                },
                                {
                                    "answer": "1"
                                }
                            ],
                            "question": "What's the answer to all questions?"
                        },
                        {
                            "answers": [
                                {
                                    "answer": "33"
                                },
                                {
                                    "answer": "42"
                                },
                                {
                                    "answer": "1"
                                }
                            ],
                            "question": "What's the answer to all questions?"
                        }
                    ]
                },
                {
                    "id": 1,
                    "questions": [
                        {
                            "answers": [
                                {
                                    "answer": "Fred"
                                },
                                {
                                    "answer": "Barney"
                                },
                                {
                                    "answer": "Dyno"
                                }
                            ],
                            "question": "Who's Wilma's husband?"
                        },
                        {
                            "answers": [
                                {
                                    "answer": "Wilma"
                                },
                                {
                                    "answer": "Pebbles"
                                },
                                {
                                    "answer": "Betty"
                                }
                            ],
                            "question": "Who's Fred's daughter?"
                        },
                        {
                            "answers": [
                                {
                                    "answer": "Dyno"
                                },
                                {
                                    "answer": "Brontosaure"
                                },
                                {
                                    "answer": "BamBam"
                                }
                            ],
                            "question": "Who's Flintstones' pet?"
                        }
                    ]
                },
                {
                    "id": 2,
                    "questions": [
                        {
                            "answers": [
                                {
                                    "answer": "Fred"
                                },
                                {
                                    "answer": "Barney"
                                },
                                {
                                    "answer": "Dyno"
                                }
                            ],
                            "question": "Who's Wilma's husband?"
                        },
                        {
                            "answers": [
                                {
                                    "answer": "Wilma"
                                },
                                {
                                    "answer": "Pebbles"
                                },
                                {
                                    "answer": "Betty"
                                }
                            ],
                            "question": "Who's Fred's daughter?"
                        },
                        {
                            "answers": [
                                {
                                    "answer": "Dyno"
                                },
                                {
                                    "answer": "Brontosaure"
                                },
                                {
                                    "answer": "BamBam"
                                }
                            ],
                            "question": "Who's Flintstones' pet?"
                        }
                    ]
                }
            ]
        })

    def test2(self):  # /quiz
        app = tested_app.test_client()

        # retrieve existing quiz 
        reply = app.get('/quiz/2')
        body = json.loads(str(reply.data, 'utf8'))
        self.assertEqual(body, {
            "id": 2,
            "questions": [
                {
                    "answers": [
                        {
                            "answer": "Fred"
                        },
                        {
                            "answer": "Barney"
                        },
                        {
                            "answer": "Dyno"
                        }
                    ],
                    "question": "Who's Wilma's husband?"
                },
                {
                    "answers": [
                        {
                            "answer": "Wilma"
                        },
                        {
                            "answer": "Pebbles"
                        },
                        {
                            "answer": "Betty"
                        }
                    ],
                    "question": "Who's Fred's daughter?"
                },
                {
                    "answers": [
                        {
                            "answer": "Dyno"
                        },
                        {
                            "answer": "Brontosaure"
                        },
                        {
                            "answer": "BamBam"
                        }
                    ],
                    "question": "Who's Flintstones' pet?"
                }
            ]
        })

        # retrieve non-existing quiz GET
        reply = app.get('/quiz/12')
        self.assertEqual(reply.status_code, 404)
        body = json.loads(str(reply.data, 'utf8'))
        self.assertEqual(body['code'], 404)

        # get question
        reply = app.get('/quiz/2/question', content_type='application/json')

        body = json.loads(str(reply.data, 'utf8'))

        self.assertEqual(body, {
            "answers": [
                {
                    "answer": "Fred"
                },
                {
                    "answer": "Barney"
                },
                {
                    "answer": "Dyno"
                }
            ],
            "question": "Who's Wilma's husband?"
        }
        )

        # correct answer
        reply = app.put('/quiz/2/question/Fred',
                        content_type='application/json')

        body = json.loads(str(reply.data, 'utf8'))

        self.assertEqual(body, {"msg": 1})

        # get question
        reply = app.get('/quiz/2/question', content_type='application/json')

        body = json.loads(str(reply.data, 'utf8'))

        self.assertEqual(body, {
            "answers": [
                {
                    "answer": "Wilma"
                },
                {
                    "answer": "Pebbles"
                },
                {
                    "answer": "Betty"
                }
            ],
            "question": "Who's Fred's daughter?"
        }
        )
        # answer ok
        reply = app.put('/quiz/2/question/Pebbles',
                        content_type='application/json')

        body = json.loads(str(reply.data, 'utf8'))

        self.assertEqual(reply.status_code, 200)
        self.assertEqual(body, {
            "msg": 2
        }
        )

        # answer ok: won a million clams
        reply = app.put('/quiz/2/question/Dyno',
                        content_type='application/json')

        body = json.loads(str(reply.data, 'utf8'))

        self.assertEqual(reply.status_code, 200)
        self.assertEqual(body, {
            "msg": "you won 1 million clams!"
        }
        )
        # double call to complete quiz
        reply = app.get('/quiz/2/question', content_type='application/json')

        body = json.loads(str(reply.data, 'utf8'))

        self.assertEqual(reply.status_code, 200)
        self.assertEqual(body, {"msg": "completed quiz"})

        # double call to complete quiz question with answer
        reply = app.put('/quiz/2/question/ciao',
                        content_type='application/json')
        body = json.loads(str(reply.data, 'utf8'))

        self.assertEqual(reply.status_code, 200)
        self.assertEqual(body, {"msg": "completed quiz"})

        # vote non-existing option
        reply = app.put('/quiz/1/question/35', content_type='application/json')

        body = json.loads(str(reply.data, 'utf8'))
        self.assertEqual(reply.status_code, 200)

        self.assertEqual(body, {"msg": "non-existing answer!"})

        # correct answer
        reply = app.put('/quiz/0/question/42', content_type='application/json')

        body = json.loads(str(reply.data, 'utf8'))
        self.assertEqual(reply.status_code, 200)
        self.assertEqual(body, {
            "msg": 1
        }
        )

        # wrong answer
        reply = app.put('/quiz/0/question/1', content_type='application/json')

        body = json.loads(str(reply.data, 'utf8'))
        self.assertEqual(body, {
            "msg": "you lost!"
        }
        )
        # double call to lost quiz
        reply = app.put('/quiz/0/question/21', content_type='application/json')

        body = json.loads(str(reply.data, 'utf8'))
        self.assertEqual(body, {
            "msg": "you lost!"
        }
        )
        # triple call to lost quiz
        reply = app.get('/quiz/0/question', content_type='application/json')

        body = json.loads(str(reply.data, 'utf8'))
        self.assertEqual(body, {"msg": "you lost!"})

        # delete quiz
        reply = app.delete('/quiz/2')
        body = json.loads(str(reply.data, 'utf8'))
        self.assertEqual(body, {
            "answered_questions": 4,
            "total_questions": 3
        }
        )

        # two loaded quizzes
        reply = app.get('/quizzes/loaded')
        body = json.loads(str(reply.data, 'utf8'))
        self.assertEqual(body['loaded_quizzes'], 2)

        reply = app.get('/quizzes')
        body = json.loads(str(reply.data, 'utf8'))
        self.assertEqual(body, {
            "loadedquizzes": [
                {
                    "id": 0,
                    "questions": [
                        {
                            "answers": [
                                {
                                    "answer": "33"
                                },
                                {
                                    "answer": "42"
                                },
                                {
                                    "answer": "1"
                                }
                            ],
                            "question": "What's the answer to all questions?"
                        },
                        {
                            "answers": [
                                {
                                    "answer": "33"
                                },
                                {
                                    "answer": "42"
                                },
                                {
                                    "answer": "1"
                                }
                            ],
                            "question": "What's the answer to all questions?"
                        }
                    ]
                },
                {
                    "id": 1,
                    "questions": [
                        {
                            "answers": [
                                {
                                    "answer": "Fred"
                                },
                                {
                                    "answer": "Barney"
                                },
                                {
                                    "answer": "Dyno"
                                }
                            ],
                            "question": "Who's Wilma's husband?"
                        },
                        {
                            "answers": [
                                {
                                    "answer": "Wilma"
                                },
                                {
                                    "answer": "Pebbles"
                                },
                                {
                                    "answer": "Betty"
                                }
                            ],
                            "question": "Who's Fred's daughter?"
                        },
                        {
                            "answers": [
                                {
                                    "answer": "Dyno"
                                },
                                {
                                    "answer": "Brontosaure"
                                },
                                {
                                    "answer": "BamBam"
                                }
                            ],
                            "question": "Who's Flintstones' pet?"
                        }
                    ]
                }
            ]
        })

        # delete previously deleted quiz
        reply = app.delete('/quiz/2')
        body = json.loads(str(reply.data, 'utf8'))
        self.assertEqual(reply.status_code, 410)

        # delete non-existing quiz
        reply = app.delete('/quiz/12')
        body = json.loads(str(reply.data, 'utf8'))
        self.assertEqual(reply.status_code, 404)

        # get previously existing quiz
        reply = app.get('/quiz/2')
        body = json.loads(str(reply.data, 'utf8'))
        self.assertEqual(reply.status_code, 410)

        # create new quiz after deletion
        reply = app.post('/quizzes',
                         data=json.dumps({
                             "questions": [
                                 {
                                     "question": "What's the answer to all questions?",
                                     "answers": [
                                         {
                                             "answer": "33",
                                             "correct": 0
                                         },
                                         {
                                             "answer": "42",
                                             "correct": 1
                                         },
                                         {
                                             "answer": "1",
                                             "correct": 0
                                         }
                                     ]
                                 },
                                 {
                                     "question": "What's the answer to all questions?",
                                     "answers": [
                                         {
                                             "answer": "33",
                                             "correct": 0
                                         },
                                         {
                                             "answer": "42",
                                             "correct": 1
                                         },
                                         {
                                             "answer": "1",
                                             "correct": 0
                                         }
                                     ]
                                 }
                             ]
                         }),
                         content_type='application/json')

        body = json.loads(str(reply.data, 'utf8'))

        self.assertEqual(body['quiznumber'], 3)

        reply = app.get('/quizzes')
        body = json.loads(str(reply.data, 'utf8'))

        self.assertEqual(body, {
            "loadedquizzes": [
                {
                    "id": 0,
                    "questions": [
                        {
                            "answers": [
                                {
                                    "answer": "33"
                                },
                                {
                                    "answer": "42"
                                },
                                {
                                    "answer": "1"
                                }
                            ],
                            "question": "What's the answer to all questions?"
                        },
                        {
                            "answers": [
                                {
                                    "answer": "33"
                                },
                                {
                                    "answer": "42"
                                },
                                {
                                    "answer": "1"
                                }
                            ],
                            "question": "What's the answer to all questions?"
                        }
                    ]
                },
                {
                    "id": 1,
                    "questions": [
                        {
                            "answers": [
                                {
                                    "answer": "Fred"
                                },
                                {
                                    "answer": "Barney"
                                },
                                {
                                    "answer": "Dyno"
                                }
                            ],
                            "question": "Who's Wilma's husband?"
                        },
                        {
                            "answers": [
                                {
                                    "answer": "Wilma"
                                },
                                {
                                    "answer": "Pebbles"
                                },
                                {
                                    "answer": "Betty"
                                }
                            ],
                            "question": "Who's Fred's daughter?"
                        },
                        {
                            "answers": [
                                {
                                    "answer": "Dyno"
                                },
                                {
                                    "answer": "Brontosaure"
                                },
                                {
                                    "answer": "BamBam"
                                }
                            ],
                            "question": "Who's Flintstones' pet?"
                        }
                    ]
                },
                {
                    "id": 3,
                    "questions": [
                        {
                            "answers": [
                                {
                                    "answer": "33"
                                },
                                {
                                    "answer": "42"
                                },
                                {
                                    "answer": "1"
                                }
                            ],
                            "question": "What's the answer to all questions?"
                        },
                        {
                            "answers": [
                                {
                                    "answer": "33"
                                },
                                {
                                    "answer": "42"
                                },
                                {
                                    "answer": "1"
                                }
                            ],
                            "question": "What's the answer to all questions?"
                        }
                    ]
                }
            ]
        })

        # delete quiz
        reply = app.delete('/quiz/1')
        body = json.loads(str(reply.data, 'utf8'))
        self.assertEqual(body, {
            "answered_questions": 0,
            "total_questions": 3
        }
        )
