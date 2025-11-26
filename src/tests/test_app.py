import unittest
from util import validate_year, UserInputError

class TestValidation(unittest.TestCase):
    def setUp(self):
        pass

    def test_year_is_positive_integer(self):
        validate_year(2020)

    def test_year_is_negative_integer(self):
        with self.assertRaises(UserInputError):
            validate_year(-5)

    def test_year_is_non_integer(self):
        with self.assertRaises(UserInputError):
            validate_year("abc")
