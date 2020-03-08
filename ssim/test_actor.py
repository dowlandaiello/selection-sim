import unittest
from actor import Condition

class TestCondition(unittest.TestCase):
    '''A class used to test the functionality of the Condition helper type'''

    def test_is_active(self):
        cond = Condition.EQ

        # The condition must be true if two ints are equal
        self.assertEqual(cond.is_active(0, 0), True)
        self.assertEqual(cond.is_active(0, 1), False)

        cond = Condition.NE

        # The condition must be true if two ints are unequal
        self.assertEqual(cond.is_active(0, 1), True)
        self.assertEqual(cond.is_active(0, 0), False)

        cond = Condition.GE

        # The condition must be true only if two ints are equal or the first
        # is greater than the second
        self.assertEqual(cond.is_active(1, 0), True)
        self.assertEqual(cond.is_active(1, 1), True)
        self.assertEqual(cond.is_active(1, 2), False)

        cond = Condition.G

        # The condition must be true only if the first of two ints is greater
        # than the second
        self.assertEqual(cond.is_active(1, 0), True)
        self.assertEqual(cond.is_active(1, 1), False)
        self.assertEqual(cond.is_active(1, 2), False)

        cond = Condition.LE

        # The condition must be true only if the first of two ints is less than
        # or equal to the second
        self.assertEqual(cond.is_active(0, 1), True)
        self.assertEqual(cond.is_active(0, 0), True)
        self.assertEqual(cond.is_active(1, 0), False)

        cond = Condition.L

        # The condition must be true only if the first of two ints is less than
        # the second
        self.assertEqual(cond.is_active(0, 1), True)
        self.assertEqual(cond.is_active(1, 1), False)
        self.assertEqual(cond.is_active(1, 0), False)

    def test_random(self):
        # Make a table that should let us only generate eq conditions
        weights = [1.0, 0, 0, 0, 0, 0]

        for _ in range(100):
            # Generate a random condition
            cond = Condition.random(weights)

            # Only eq conditions should be generated, as the weight table stipulates so
            self.assertEqual(cond.value, 1)

class TestModifier(unittest.TestCase):
    '''A class used to test the functionality of the InputModifier helper type'''

    

if __name__ == '__main__':
    # Run the tests!
    unittest.main()
