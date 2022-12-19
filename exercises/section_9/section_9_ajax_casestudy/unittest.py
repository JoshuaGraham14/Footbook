import os
import unittest

def add(x,y):
    return x + y

class TestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_add_correct(self):
        assert add(3,4) == 7

    def test_add_incorrect(self):
        assert add(3,3) != 7

if __name__ == '__main__':
    unittest.main()