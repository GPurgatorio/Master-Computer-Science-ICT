import json
import unittest
import random as rnd

from flask import jsonify


class Die:

    def __init__(self, filename):
        self.faces = []
        self.pip = None
        f = open(filename, "r")
        lines = f.readlines()
        for line in lines:
            self.faces.append(line.replace("\n", ""))
        self.throw_die()
        f.close()

    def throw_die(self):
        if self.faces:  # pythonic for list is not empty
            self.pip = rnd.choice(self.faces)
            return self.pip
        else:
            raise IndexError("throw_die(): empty die error.")


class DiceSet:

    def __init__(self, dice):
        self.dice = dice
        self.pips = []

    def serialize(self):
        return json.dumps(self.pips)

    def throw_dice(self):
        if not self.pips: # check if list is empty, not assigned yet
            self.pips = [None] * (len(self.dice))
        for i in range(len(self.dice)):
            self.pips[i] = self.dice[i].throw_die()
        return self.pips


class TestDie(unittest.TestCase):

    def test_die_init(self):
        die = Die("tests/die0.txt")
        check = ['bike', 'moonandstars', 'bag', 'bird', 'crying', 'angry']
        self.assertEqual(die.faces, check)

    def test_die_pip(self):
        rnd.seed(574891)
        die = Die("tests/die0.txt")
        res = die.throw_die()
        self.assertEqual(res, 'bag')


if __name__ == '__main__':
    unittest.main()
