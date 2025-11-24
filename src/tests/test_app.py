import unittest
from util import validate_year, UserInputError

class TestValidation(unittest.TestCase):
    def setUp(self):
        pass

    def test_vuosi_on_positiivinen_integer(self):
        validate_year(2020)

    def test_vuosi_on_negatiivinen_integer(self):
        with self.assertRaises(UserInputError):
            validate_year(-5)
