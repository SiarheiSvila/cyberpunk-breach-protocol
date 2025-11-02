import unittest
from find_sequences import all_merged_sequences


class TestAllMergedSequences(unittest.TestCase):
    def test_empty_daemons(self):
        """Test with an empty list of daemons."""
        self.assertEqual(all_merged_sequences([], 5), {})

    def test_single_daemon(self):
        """Test with a single daemon that is within the buffer size."""
        daemons = [["A", "B"]]
        buffer_size = 3
        expected = {(0,): ["A", "B"]}
        self.assertEqual(all_merged_sequences(daemons, buffer_size), expected)

    def test_daemon_exceeds_buffer(self):
        """Test with a single daemon that exceeds the buffer size."""
        daemons = [["A", "B", "C"]]
        buffer_size = 2
        self.assertEqual(all_merged_sequences(daemons, buffer_size), {})

    def test_simple_merge(self):
        """Test a simple merge of two daemons."""
        daemons = [["A", "B"], ["B", "C"]]
        buffer_size = 3
        expected = {
            (0,): ["A", "B"],
            (1,): ["B", "C"],
            (0, 1): ["A", "B", "C"],
        }
        self.assertEqual(all_merged_sequences(daemons, buffer_size), expected)

    def test_merge_exceeds_buffer(self):
        """Test when merging two daemons exceeds the buffer size."""
        daemons = [["A", "B"], ["C", "D"]]
        buffer_size = 3
        expected = {
            (0,): ["A", "B"],
            (1,): ["C", "D"],
        }
        # The merged sequence "ABCD" is 4, so it should not be in the result
        self.assertEqual(all_merged_sequences(daemons, buffer_size), expected)


if __name__ == "__main__":
    unittest.main()
