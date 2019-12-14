class TestUtils(unittest.TestCase):
    """Test cases for various utility functions."""

    def test_trim_suggestions(self):
        word = "gud"
        suggs = ["good", "god", "bad+"]
        self.assertEqual(trim_suggestions(word, suggs, 40), ["god", "good", "bad+"])
        self.assertEqual(trim_suggestions(word, suggs, 4), ["god", "good", "bad+"])
        self.assertEqual(trim_suggestions(word, suggs, 3), ["god", "good", "bad+"])
        self.assertEqual(trim_suggestions(word, suggs, 2), ["god", "good"])
        self.assertEqual(trim_suggestions(word, suggs, 1), ["god"])
        self.assertEqual(trim_suggestions(word, suggs, 0), [])
