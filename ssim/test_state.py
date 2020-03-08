import unittest
from state import Mutation

class TestMutation(unittest.TestCase):
    '''A class used to test the functionality of the Mutation helper type'''

    def test_random(self):
        for _ in range(100):
            # Always generate an injection mutation, since the table stipulates as such
            self.assertEqual(Mutation.random([1.0, 0.0]), Mutation.INJECT)

if __name__ == '__main__':
    # Run the tests!
    unittest.main()
