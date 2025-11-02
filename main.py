from typing import List, Dict, Tuple

from helpers.find_sequences import all_merged_sequences
from helpers.find_match_in_matrix import find_sequence_path
from helpers.cover_finder import find_minimum_cover


def print_sequences(sequences: List[Tuple[Tuple[int, ...], Dict]], matrix: List[List[str]]):
    """
    Prints the sequences along with a visualization of their paths in the matrix.
    """
    if not sequences:
        print("\nNo valid sequences found to display.")
        return

    def create_path_matrix(path: List[Tuple[int, int]]) -> List[List[str]]:
        """
        Creates a new matrix that highlights the given path.
        Elements on the path retain their original value, while others are marked as 'XX'.
        """
        path_set = set(path)
        return [
            [matrix[r][c] if (r, c) in path_set else "XX" for c in range(len(matrix[0]))]
            for r in range(len(matrix))
        ]

    print("\n--- Found Sequences ---")
    for daemon_indices, info in sequences:
        print(f"\nDaemons covered: {daemon_indices}")
        print(f"Sequence: {' '.join(info['sequence'])}")
        print("Path:")
        for row in create_path_matrix(info["path"]):
            print(f"  {' '.join(row)}")


def find_matching_sequences(matrix: List[List[str]], daemons: List[List[str]], buffer_size: int):
    """
    Main orchestrator function.
    It finds all valid merged sequences, filters them, finds the minimum cover, and prints the result.
    """
    # Step 1: Generate all possible merged sequences of daemons
    merged_sequences = all_merged_sequences(daemons, buffer_size)

    # Step 2: Filter these sequences to keep only those with a valid path in the matrix
    found_sequences = {
        indices: {"sequence": sequence, "path": path}
        for indices, sequence in merged_sequences.items()
        if (path := find_sequence_path(matrix, sequence, buffer_size))
    }

    # Step 3: Find the minimum set of sequences to cover all (or as many as possible) daemons
    min_cover = find_minimum_cover(found_sequences, len(daemons))

    # Step 4: Print the results
    if min_cover:
        print_sequences(min_cover, matrix)
    else:
        print("\nCould not find a sequence combination to cover any daemons.")
