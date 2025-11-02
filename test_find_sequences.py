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

    def test_small_buffer_size(self):
        daemons = [
            ["1C", "BD"],
            ["BD", "55"],
            ["55", "E9"]
        ]
        buffer_size = 3

        expected_sequences = {
            (0,): ["1C", "BD"],
            (1,): ["BD", "55"],
            (2,): ["55", "E9"],
            (0, 1): ["1C", "BD", "55"],
            (1, 2): ["BD", "55", "E9"],
        }

        result = all_merged_sequences(daemons, buffer_size)
        self.assertEqual(result, expected_sequences)

    def test_no_overlapping_sequences(self):
        daemons = [
            ["1C", "BD"],
            ["55", "E9"]
        ]
        buffer_size = 4

        expected_sequences = {
            (0,): ["1C", "BD"],
            (1,): ["55", "E9"],
            (0, 1): ["1C", "BD", "55", "E9"],
        }

        result = all_merged_sequences(daemons, buffer_size)
        self.assertEqual(result, expected_sequences)

    def test_multiple_daemons_with_same_sequence(self):
        daemons = [
            ["1C", "BD"],
            ["1C", "BD"]
        ]
        buffer_size = 2

        expected_sequences = {
            (0, 1): ["1C", "BD"]
        }

        result = all_merged_sequences(daemons, buffer_size)
        self.assertEqual(result, expected_sequences)

if __name__ == "__main__":
    unittest.main()
