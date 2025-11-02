import unittest
from find_match_in_matrix import find_sequence_path

class TestFindMatchInMatrix(unittest.TestCase):
    def test_find_sequence_path(self):
        matrix = [
            ['1C', 'BD', '1C', '55', 'E9'],
            ['1C', '1C', '55', '7A', '1C'],
            ['1C', 'E9', 'BD', 'BD', '7A'],
            ['BD', '1C', '1C', 'E9', '1C'],
            ['7A', 'E9', 'E9', 'E9', '1C']
        ]
        sequence = ["1C", "55", "BD"]
        buffer_size = 5

        expected_path = [(1, 0), (1, 2), (2, 2)]

        result = find_sequence_path(matrix, sequence, buffer_size)
        self.assertEqual(result, expected_path)

    def test_find_sequence_path_not_found(self):
        matrix = [
            ['1C', 'BD'],
            ['E9', '55']
        ]
        sequence = ["1C", "7A"]
        buffer_size = 3

        result = find_sequence_path(matrix, sequence, buffer_size)
        self.assertEqual(result, [])

    def test_empty_matrix(self):
        matrix = []
        sequence = ["1C", "55", "BD"]
        buffer_size = 5

        with self.assertRaises(IndexError):
            find_sequence_path(matrix, sequence, buffer_size)

    def test_sequence_found_multiple_times(self):
        matrix = [
            ['1C', '55', 'BD', '1C', '55'],
            ['BD', '1C', '55', 'BD', '1C'],
            ['55', 'BD', '1C', '55', 'BD']
        ]
        sequence = ["1C", "55", "BD"]
        buffer_size = 3

        possible_paths = [
            [(0, 0), (0, 1), (0, 2)],
            [(1, 1), (1, 2), (1, 3)],
            [(2, 2), (2, 3), (2, 4)],
            [(0, 0), (2, 0), (2, 1)]
        ]

        result = find_sequence_path(matrix, sequence, buffer_size)
        self.assertIn(result, possible_paths)

if __name__ == "__main__":
    unittest.main()
