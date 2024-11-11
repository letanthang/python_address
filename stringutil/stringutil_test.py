import unittest
from stringutil import is_integer, reverse_string, remove_delimiter

class TestStringUtil(unittest.TestCase):

    def test_is_integer(self):
        cases = [
            {"args": "123", "want": True},
            {"args": "123.1", "want": False},
            {"args": "abc", "want": False},
            {"args": "123abc", "want": False},
        ]
        for case in cases:
            with self.subTest(case=case):
                got = is_integer(case["args"])
                self.assertEqual(got, case["want"], f"is_integer({case['args']}) == {got}, want {case['want']}")

    def test_reverse_string(self):
        cases = [
            {"args": "123", "want": "321"},
            {"args": "123.1", "want": "1.321"},
            {"args": "abc", "want": "cba"},
            {"args": "123abc", "want": "cba321"},
        ]
        for case in cases:
            with self.subTest(case=case):
                got = reverse_string(case["args"])
                self.assertEqual(got, case["want"], f"reverse_string({case['args']}) == {got}, want {case['want']}")

    def test_remove_delimiter(self):
        cases = [
            {"args": "ab,c", "want": "abc"},
            {"args": "123.abc", "want": "123abc"},
            {"args": "123.abc", "want": "123abc"},
        ]
        for case in cases:
            with self.subTest(case=case):
                got = remove_delimiter(case["args"])
                self.assertEqual(got, case["want"], f"remove_delimiter({case['args']}) == {got}, want {case['want']}")

if __name__ == "__main__":
    unittest.main()