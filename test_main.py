import unittest
from main import find_matching_sequences, find_minimum_cover


class TestMain(unittest.TestCase):
    def test_main_1(self):
        matrix = [
            ['1C', 'BD', '1C', '55', 'E9'],
            ['1C', '1C', '55', '7A', '1C'],
            ['1C', 'E9', 'BD', 'BD', '7A'],
            ['BD', '1C', '1C', 'E9', '1C'],
            ['7A', 'E9', 'E9', 'E9', '1C']
        ]

        daemons = [
            ["BD", "7A", "E9"],
            ["1C", "55", "BD", "7A", "E9"],
            ["55", "BD", "7A"]
        ]
        buffer_size = 5
        find_matching_sequences(matrix, daemons, buffer_size)

    def test_main_2(self):
        matrix = [
            ["BD", "E9", "1C", "BD", "BD"],
            ["1C", "1C", "BD", "BD", "55"],
            ["BD", "BD", "55", "BD", "BD"],
            ["1C", "55", "55", "E9", "BD"],
            ["55", "1C", "BD", "55", "55"]
        ]

        daemons = [
            ["55", "1C"],  # Datamine_V1
            ["1C", "E9", "BD"],  # Datamine_V2
            ["BD", "BD", "55"]  # Datamine_V3
        ]
        buffer_size = 6
        find_matching_sequences(matrix, daemons, buffer_size)

class TestFindMinimumCover(unittest.TestCase):
    def test_find_minimum_cover_perfect_cover(self):
        found_sequences = {
            (0,): {"sequence": ["1C", "BD"], "path": []},
            (1, 2): {"sequence": ["BD", "55", "E9"], "path": []}
        }
        num_daemons = 3

        expected_cover = [
            ((0,), {"sequence": ["1C", "BD"], "path": []}),
            ((1, 2), {"sequence": ["BD", "55", "E9"], "path": []})
        ]

        result = find_minimum_cover(found_sequences, num_daemons)
        self.assertCountEqual(result, expected_cover)

    def test_find_minimum_cover_partial_cover(self):
        found_sequences = {
            (0,): {"sequence": ["1C", "BD"], "path": []},
            (1,): {"sequence": ["BD", "55"], "path": []}
        }
        num_daemons = 3

        expected_cover = [
            ((0,), {"sequence": ["1C", "BD"], "path": []}),
            ((1,), {"sequence": ["BD", "55"], "path": []})
        ]

        result = find_minimum_cover(found_sequences, num_daemons)
        self.assertCountEqual(result, expected_cover)

    def test_find_minimum_cover_empty(self):
        found_sequences = {}
        num_daemons = 3

        result = find_minimum_cover(found_sequences, num_daemons)
        self.assertEqual(result, [])

    def test_no_cover_found(self):
        found_sequences = {
            (0,): {"sequence": ["1C", "BD"], "path": []}
        }
        num_daemons = 3

        expected_cover = [((0,), {"sequence": ["1C", "BD"], "path": []})]

        result = find_minimum_cover(found_sequences, num_daemons)
        self.assertEqual(result, expected_cover)

    def test_perfect_cover_with_multiple_combinations(self):
        found_sequences = {
            (0,): {"sequence": ["1C", "BD"], "path": []},
            (1,): {"sequence": ["BD", "55"], "path": []},
            (0, 1): {"sequence": ["1C", "BD", "55"], "path": []}
        }
        num_daemons = 2

        expected_cover = [((0, 1), {"sequence": ["1C", "BD", "55"], "path": []})]

        result = find_minimum_cover(found_sequences, num_daemons)
        self.assertEqual(result, expected_cover)

    def test_complex_partial_cover(self):
        found_sequences = {
            (0, 1): {"sequence": ["1C", "BD", "55"], "path": []},
            (2, 3): {"sequence": ["E9", "7A"], "path": []},
            (0, 2): {"sequence": ["1C", "E9"], "path": []}
        }
        num_daemons = 4

        expected_cover = [
            ((0, 1), {"sequence": ["1C", "BD", "55"], "path": []}),
            ((2, 3), {"sequence": ["E9", "7A"], "path": []})
        ]

        result = find_minimum_cover(found_sequences, num_daemons)
        self.assertCountEqual(result, expected_cover)

if __name__ == "__main__":
    unittest.main()
