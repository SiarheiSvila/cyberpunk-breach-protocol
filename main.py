"""
This is the main module for the Cyberpunk hacking minigame solver. It orchestrates
the process of finding the optimal sequences of daemons to upload given a code
matrix, a list of daemons, and a buffer size.
"""

from itertools import combinations
from typing import List, Dict, Tuple, Set, Any

# Assuming the refactored function from find_sequences.py is named get_all_merged_sequences
from find_sequences import get_all_merged_sequences
from find_match_in_matrix import find_sequence_path

Path = List[Tuple[int, int]]
Sequence = List[str]
SequenceInfo = Dict[str, Any]

def find_minimum_cover(found_sequences: Dict[Tuple[int, ...], SequenceInfo], num_daemons: int) -> List[Tuple[Tuple[int, ...], SequenceInfo]]:
    """
    Finds the minimum number of sequences that cover all daemons.

    If a complete cover that includes all daemons is not possible, this function
    returns the combination of sequences that covers the maximum number of unique daemons.

    Args:
        found_sequences: A dictionary where keys are tuples of daemon indices covered
                         and values are dictionaries containing sequence info (e.g., path).
        num_daemons: The total number of daemons to be covered.

    Returns:
        A list of tuples, where each tuple contains the covered daemon indices
        and their corresponding sequence information, representing the best
        possible cover.
    """
    if not found_sequences:
        return []

    all_daemons_set = set(range(num_daemons))
    
    # Prepare a list of items for combination, each is (daemon_indices, info)
    sequence_items = list(found_sequences.items())
    
    best_cover = []
    max_daemons_covered = 0

    # Iterate through all possible combination sizes, from 1 to all sequences
    for size in range(1, len(sequence_items) + 1):
        for combo in combinations(sequence_items, size):
            # Collect all unique daemons covered by this combination
            covered_daemons: Set[int] = set()
            for daemon_indices, _ in combo:
                covered_daemons.update(daemon_indices)

            # If this combination covers all daemons, it's an optimal solution
            if covered_daemons == all_daemons_set:
                return list(combo)
            
            # Otherwise, check if it's the best partial cover found so far
            if len(covered_daemons) > max_daemons_covered:
                max_daemons_covered = len(covered_daemons)
                best_cover = list(combo)
    
    return best_cover

def print_sequences(sequences: List[Tuple[Tuple[int, ...], SequenceInfo]], matrix: List[List[str]]):
    """
    Prints the details of the selected sequences, including a visualization
    of their path through the matrix.

    Args:
        sequences: A list of tuples, each containing daemon indices and sequence info.
        matrix: The original code matrix for visualization.
    """
    def create_path_matrix(path: Path) -> List[List[str]]:
        """
        Creates a new matrix where only the elements of the path are shown,
        and all other elements are replaced with 'XX' for clarity.
        """
        path_set = set(path)
        return [
            [matrix[r][c] if (r, c) in path_set else 'XX' for c in range(len(matrix[0]))]
            for r in range(len(matrix))
        ]

    print("\n--- Optimal Sequence Cover ---")
    for daemon_indices, info in sequences:
        print(f"\nDaemons covered: {daemon_indices}")
        print(f"Sequence: {' '.join(info['sequence'])}")
        print("Path:")
        path_matrix = create_path_matrix(info['path'])
        for row in path_matrix:
            print(f"  {' '.join(row)}")

def find_matching_sequences(matrix: List[List[str]], daemons: List[List[str]], buffer_size: int):
    """
    Main function to solve the hacking minigame.

    This function takes the code matrix, a list of daemons, and the buffer size,
    then finds the optimal set of sequences to execute.

    Args:
        matrix: The 2D grid of characters.
        daemons: A list of daemon sequences to find.
        buffer_size: The maximum length of a sequence path.
    """
    # Step 1: Generate all possible merged sequences that can be formed from the daemons
    merged_sequences = get_all_merged_sequences(daemons, buffer_size)
    
    # Step 2: For each merged sequence, check if it can be found in the matrix
    found_sequences: Dict[Tuple[int, ...], SequenceInfo] = {}
    for daemon_indices, sequence in merged_sequences.items():
        path = find_sequence_path(matrix, sequence, buffer_size)
        if path:
            found_sequences[daemon_indices] = {"sequence": sequence, "path": path}

    # Step 3: Find the minimum set of sequences that covers the most daemons
    min_cover = find_minimum_cover(found_sequences, len(daemons))
    
    # Step 4: Print the results
    if min_cover:
        print_sequences(min_cover, matrix)
    else:
        print("\nNo valid sequences can be found in the matrix.")
