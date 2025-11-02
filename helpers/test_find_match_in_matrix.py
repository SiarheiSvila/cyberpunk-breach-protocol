"""
Unit tests for the find_match_in_matrix module.
"""
import unittest
from helpers.find_match_in_matrix import find_sequence_path


class TestFindSequencePath(unittest.TestCase):
    """
    Test suite for the find_sequence_path function.
    """

    def test_simple_path(self):
        """Test a simple path that can be found in the matrix."""
        matrix = [
            ["A", "B", "C"],
            ["D", "E", "F"],
            ["G", "H", "I"],
        ]
        sequence = ["A", "D", "E"]
        buffer_size = 5
        expected = [(0, 0), (1, 0), (1, 1)]
        self.assertEqual(find_sequence_path(matrix, sequence, buffer_size), expected)

    def test_path_not_found(self):
        """Test when the sequence cannot be found in the matrix."""
        matrix = [
            ["A", "B"],
            ["C", "D"],
        ]
        sequence = ["A", "D"]
        buffer_size = 3
        self.assertEqual(find_sequence_path(matrix, sequence, buffer_size), [])

    def test_buffer_too_small(self):
        """Test when the path exists but is longer than the buffer size."""
        matrix = [
            ["A", "B", "C"],
            ["D", "E", "F"],
        ]
        sequence = ["A", "D", "E"]
        buffer_size = 2
        self.assertEqual(find_sequence_path(matrix, sequence, buffer_size), [])

    def test_alternative_paths(self):
        """Test that the function finds the first valid path."""
        matrix = [
            ["A", "B"],
            ["A", "D"],
        ]
        sequence = ["A", "D"]
        buffer_size = 3
        # It should find the path starting at (0, 0) and going to (1, 1) via (1, 0)
        expected = [(1, 0), (1, 1)]
        self.assertEqual(find_sequence_path(matrix, sequence, buffer_size), expected)


if __name__ == "__main__":
    unittest.main()
