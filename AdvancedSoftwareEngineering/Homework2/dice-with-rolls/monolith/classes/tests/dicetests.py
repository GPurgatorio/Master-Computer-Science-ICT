from monolith.classes.DiceSet import Die
import unittest


class TestDie(unittest.TestCase):
 
    def test_add_integers_positive(self):
        die = Die("die0.txt")
        rnd.seed(574891)
        print(die.faces)
        self.assertEqual(result, 3)

 
if __name__ == '__main__':
    unittest.main()
