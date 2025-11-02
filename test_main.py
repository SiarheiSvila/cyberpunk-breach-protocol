"""
Unit tests for the main script.
"""
import unittest
from main import find_matching_sequences


class TestMain(unittest.TestCase):
    """
    Test suite for the find_matching_sequences function.
    """

    def test_main_1(self):
        """
        Test case with a specific matrix and daemons.
        """
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
        """
        Another test case with a different matrix and daemons.
        """
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


if __name__ == "__main__":
    unittest.main()
