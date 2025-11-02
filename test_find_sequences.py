import unittest
from find_sequences import all_merged_sequences

class TestFindSequences(unittest.TestCase):
    def test_all_merged_sequences(self):
        daemons = [
            ["1C", "BD"],
            ["BD", "55"],
            ["55", "E9"]
        ]
        buffer_size = 4

        expected_sequences = {
            (0,): ["1C", "BD"],
            (1,): ["BD", "55"],
            (2,): ["55", "E9"],
            (0, 1): ["1C", "BD", "55"],
            (1, 2): ["BD", "55", "E9"],
            (0, 2): ["55", "E9", "1C", "BD"],
            (0, 1, 2): ["1C", "BD", "55", "E9"],
        }

        result = all_merged_sequences(daemons, buffer_size)

        self.assertEqual(len(result), len(expected_sequences))
        for key, value in expected_sequences.items():
            self.assertIn(key, result)
            self.assertEqual(result[key], value)

if __name__ == "__main__":
    unittest.main()
