import unittest
from cover_finder import find_minimum_cover


class TestFindMinimumCover(unittest.TestCase):
    def test_empty_case(self):
        """Test with no found sequences."""
        self.assertEqual(find_minimum_cover({}, 5), [])

    def test_simple_cover(self):
        """Test a straightforward case with a single sequence covering all daemons."""
        found_sequences = {
            (0, 1): {"sequence": ["A", "B"], "path": [(0, 0), (1, 0)]}
        }
        num_daemons = 2
        expected = [((0, 1), {"sequence": ["A", "B"], "path": [(0, 0), (1, 0)]})]
        self.assertEqual(find_minimum_cover(found_sequences, num_daemons), expected)

    def test_no_complete_cover(self):
        """Test when no combination of sequences can cover all daemons."""
        found_sequences = {
            (0,): {"sequence": ["A"], "path": [(0, 0)]},
            (1,): {"sequence": ["B"], "path": [(1, 1)]},
        }
        num_daemons = 3
        # Should return the combination that covers the most daemons
        result = find_minimum_cover(found_sequences, num_daemons)
        self.assertIn(
            ((0,), {"sequence": ["A"], "path": [(0, 0)]}),
            result,
        )

    def test_multiple_sequences_form_cover(self):
        """Test when two sequences are needed to form a complete cover."""
        found_sequences = {
            (0, 1): {"sequence": ["A", "B"], "path": [(0, 0), (1, 0)]},
            (2, 3): {"sequence": ["C", "D"], "path": [(0, 1), (1, 1)]},
        }
        num_daemons = 4
        result = find_minimum_cover(found_sequences, num_daemons)
        self.assertEqual(len(result), 2)
        # The order is not guaranteed, so check for presence of both items
        self.assertIn(((0, 1), {"sequence": ["A", "B"], "path": [(0, 0), (1, 0)]}), result)
        self.assertIn(((2, 3), {"sequence": ["C", "D"], "path": [(0, 1), (1, 1)]}), result)


if __name__ == "__main__":
    unittest.main()
