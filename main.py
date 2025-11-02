from itertools import combinations
from typing import List, Dict, Tuple, Set

from find_sequences import all_merged_sequences
from find_match_in_matrix import find_sequence_path

# A set of daemon indices, e.g., {0, 2, 3}
DaemonSet = Set[int]
# A tuple representing a combination of daemon sets, e.g., ((0, 1), (2,))
DaemonSetCombination = Tuple[DaemonSet, ...]
# Information about a found sequence, including the sequence itself and its path
SequenceInfo = Dict[str, list]


def _find_best_cover(
    sequence_items: List[Tuple[Tuple[int, ...], DaemonSet, SequenceInfo]],
    all_daemons: DaemonSet,
) -> List[Tuple[Tuple[int, ...], SequenceInfo]]:
    """
    Find the best combination of sequences to cover the most daemons.
    """
    best_cover = []
    max_covered_count = 0

    # Check all combination sizes, from 1 to the total number of available sequences
    for size in range(1, len(sequence_items) + 1):
        for combo in combinations(sequence_items, size):
            # Union of all daemon sets in the current combination
            covered_daemons = set().union(*(daemon_set for _, daemon_set, _ in combo))

            # If this combination covers all daemons, it's a perfect cover
            if covered_daemons == all_daemons:
                return [(indices, info) for indices, _, info in combo]

            # Otherwise, check if this combination is the best one found so far
            if len(covered_daemons) > max_covered_count:
                max_covered_count = len(covered_daemons)
                best_cover = [(indices, info) for indices, _, info in combo]

    return best_cover


def find_minimum_cover(
    found_sequences: Dict[Tuple[int, ...], SequenceInfo],
    num_daemons: int,
) -> List[Tuple[Tuple[int, ...], SequenceInfo]]:
    """
    Find the minimum number of sequences that cover all daemons.
    If no complete cover is possible, return the combination that covers the most daemons.
    """
    if not found_sequences:
        return []

    # A set of all daemon indices, e.g., {0, 1, 2} for 3 daemons
    all_daemons = set(range(num_daemons))

    # Create a list of tuples, each containing daemon indices, a set of these indices, and sequence info
    sequence_items = [
        (indices, set(indices), info) for indices, info in found_sequences.items()
    ]

    return _find_best_cover(sequence_items, all_daemons)


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
