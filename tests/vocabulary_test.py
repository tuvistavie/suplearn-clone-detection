from tests.base import TestCase

from suplearn_clone_detection.vocabulary import Vocabulary



class VocabularyTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.vocab_no_values = Vocabulary(cls.fixture_path("vocab-noid.tsv"))
        cls.vocab_with_values = Vocabulary(cls.fixture_path("vocab-100.tsv"))

    def test_valid_access_no_value(self):
        self.assertEqual(self.vocab_no_values[{"type": "SimpleName"}], 0)
        self.assertEqual(self.vocab_no_values[{"type": "BinaryExpr"}], 10)
        self.assertEqual(self.vocab_no_values[{"type": "DoStmt"}], 60)

    def test_valid_access_with_value(self):
        self.assertEqual(self.vocab_with_values[{"type": "SimpleName"}], 0)
        self.assertEqual(self.vocab_with_values[{"type": "IntegerLiteralExpr", "value": "0"}], 21)
        self.assertEqual(
            self.vocab_with_values[{"type": "BooleanLiteralExpr", "value": "true"}], 67)

    def test_keyerror_no_value(self):
        with self.assertRaises(KeyError):
            _ = self.vocab_no_values[{"type": "IDontExist"}]

    def test_keyerror_with_value(self):
        with self.assertRaises(KeyError):
            _ = self.vocab_with_values[{"type": "IDontExist"}]

        with self.assertRaises(KeyError):
            _ = self.vocab_with_values[{"type": "SimpleName", "value": "dont-exist"}]
