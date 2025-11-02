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

if __name__ == "__main__":
    unittest.main()
