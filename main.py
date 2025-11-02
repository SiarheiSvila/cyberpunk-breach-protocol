from itertools import combinations
from find_sequences import all_merged_sequences
from find_match_in_matrix import find_sequence_path


def find_minimum_cover(found_sequences: dict, num_daemons: int):
    """
    Find the minimum number of sequences that cover all daemons.
    If no complete cover exists, return the combination that covers maximum daemons.
    """
    if not found_sequences:
        return []
    
    all_daemons = set(range(num_daemons))
    sequence_items = [(indices, set(indices), found_sequences[indices]) 
                      for indices in found_sequences.keys()]
    best_cover, best_count = [], 0
    
    # Try all combinations from size 1 up to the number of sequences
    for size in range(1, len(found_sequences) + 1):
        for combo in combinations(sequence_items, size):
            covered = set().union(*(daemon_set for _, daemon_set, _ in combo))
            selected = [(indices, info) for indices, _, info in combo]
            
            if covered == all_daemons:
                return selected
            
            if len(covered) > best_count:
                best_count = len(covered)
                best_cover = selected
    
    return best_cover


def print_sequences(sequences: list, matrix: list[list[str]]):
    """Print sequences with their path visualizations."""

    def create_path_matrix(matrix: list[list[str]], path: list[tuple[int, int]]) -> list[list[str]]:
        """Create a matrix where path elements keep original value, others are 'XX'."""
        path_set = set(path)
        return [[matrix[r][c] if (r, c) in path_set else 'XX' 
                for c in range(len(matrix[0]))] 
                for r in range(len(matrix))]

    for daemon_indices, info in sequences:
        print(f"Daemon indices: {daemon_indices}")
        print(f"Sequence: {info['sequence']}")
        for row in create_path_matrix(matrix, info['path']):
            print("  " + " ".join(row))
        print()


def find_matching_sequences(matrix: list[list[str]], daemons: list[list[str]], buffer_size: int):
    sequences = all_merged_sequences(daemons, buffer_size)
    
    # Filter sequences that have valid paths in the matrix
    found_sequences = {
        demons: {"sequence": sequence, "path": path}
        for demons, sequence in sequences.items()
        if (path := find_sequence_path(matrix, sequence, buffer_size))
    }

    min_cover = find_minimum_cover(found_sequences, len(daemons))
    
    if min_cover:
        print_sequences(min_cover, matrix)
    else:
        print("\nNo cover found - cannot cover any daemons with available sequences")

