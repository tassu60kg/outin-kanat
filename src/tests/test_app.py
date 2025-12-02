import unittest
from util import validate_year, validate_cite_key, generate_bibtex, UserInputError

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

class TestCiteKeyValidation(unittest.TestCase):
    def setUp(self):
        pass

    def test_cite_key_is_accepted(self):
        validate_cite_key("CBH91")

    def test_cite_key_is_empty(self):
        with self.assertRaises(UserInputError):
            validate_cite_key("")

    def test_cite_key_contains_spaces(self):
        with self.assertRaises(UserInputError):
            validate_cite_key("my key")

    def test_cite_key_contains_special_numbers(self):
        with self.assertRaises(UserInputError):
            validate_cite_key("£€$")

    def test_cite_key_is_not_string(self):
        with self.assertRaises(UserInputError):
            validate_cite_key(123)


class TestBibtexGeneration(unittest.TestCase):

    def test_article_bibtex(self):
        ref = {
            "cite_key": "CBH91",
            "type": "article",
            "author": "Allan Collins and John Seely Brown and Ann Holum",
            "title": "Cognitive apprenticeship: making thinking visible",
            "year": 1991,
            "journal": "American Educator",
            "volume": "3",
            "pages": "38–46",
            "publisher": None,
            "booktitle": None,
            "isbn": None,
        }

        bib = generate_bibtex(ref)

        self.assertTrue(bib.startswith("@article{CBH91"))
        self.assertTrue(bib.endswith("}"))

        self.assertIn("author = {Allan Collins and John Seely Brown and Ann Holum}", bib)
        self.assertIn("title = {Cognitive apprenticeship: making thinking visible}", bib)
        self.assertIn("year = {1991}", bib)
        self.assertIn("journal = {American Educator}", bib)
        self.assertIn("volume = {3}", bib)
        self.assertIn("pages = {38–46}", bib)

    def test_book_bibtex(self):
        ref = {
            "cite_key": "summerbook",
            "type": "book",
            "author": "Tove Jansson",
            "title": "The Summer Book",
            "year": 1972,
            "publisher": "WSOY",
            "journal": None,
            "volume": None,
            "pages": None,
            "booktitle": None,
            "isbn": "9789510434383",
        }

        bib = generate_bibtex(ref)

        self.assertIn("@book{summerbook", bib)
        self.assertIn("author = {Tove Jansson}", bib)
        self.assertIn("title = {The Summer Book}", bib)
        self.assertIn("year = {1972}", bib)
        self.assertIn("publisher = {WSOY}", bib)
        self.assertIn("isbn = {9789510434383}", bib)

    def test_skip_missing_optional_fields(self):
        ref = {
            "cite_key": "nash51",
            "type": "article",
            "author": "John Nash",
            "title": "Non-cooperative Games",
            "year": 1951,
        }

        bib = generate_bibtex(ref)

        self.assertIn("author = {John Nash}", bib)
        self.assertIn("title = {Non-cooperative Games}", bib)
        self.assertIn("year = {1951}", bib)

        self.assertNotIn("journal =", bib)
        self.assertNotIn("publisher =", bib)
        self.assertNotIn("volume =", bib)
        self.assertNotIn("pages =", bib)
        self.assertNotIn("isbn =", bib)

    def test_correct_formatting(self):
        ref = {
            "cite_key": "moomin",
            "type": "book",
            "author": "Tove Jansson",
            "title": "Comet in Moominland",
            "year": 1946
        }

        bib = generate_bibtex(ref)
        lines = bib.split("\n")

        self.assertTrue(lines[0].startswith("@book{moomin"))
        self.assertEqual(lines[-1], "}")
