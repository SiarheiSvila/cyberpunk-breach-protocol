"""
This module provides functions for generating all valid merged sequences of daemons
that are within a given buffer size. It explores all permutations of daemons,
merges them, and checks for their validity.
"""
from itertools import permutations
from typing import List, Dict, Tuple


def _overlap_merge(seq1: List[str], seq2: List[str]) -> List[str]:
    """
    Merges two sequences with the maximal possible suffix-prefix overlap.

    For example, merging ["A", "B", "C"] and ["B", "C", "D"] would result in ["A", "B", "C", "D"].

    Args:
        seq1: The first sequence.
        seq2: The second sequence.

    Returns:
        The merged sequence.
    """
    max_overlap = 0
    # Iterate backwards from the minimum length of the two sequences to find the largest overlap
    for i in range(min(len(seq1), len(seq2)), 0, -1):
        if seq1[-i:] == seq2[:i]:
            max_overlap = i
            break
    # Append the non-overlapping part of the second sequence to the first one
    return seq1 + seq2[max_overlap:]


def _contains_subsequence(sequence: List[str], subseq: List[str]) -> bool:
    """
    Checks if a sequence contains a given subsequence.

    Args:
        sequence: The main sequence to search within.
        subseq: The subsequence to search for.

    Returns:
        True if the subsequence is found, False otherwise.
    """
    n, m = len(sequence), len(subseq)
    # Slide a window of size m over the sequence to check for the subsequence
    for i in range(n - m + 1):
        if sequence[i : i + m] == subseq:
            return True
    return False


def all_merged_sequences(
    daemons: List[List[str]], buffer_size: int
) -> Dict[Tuple[int, ...], List[str]]:
    """
    Generates all valid merged sequences of daemons that are within the given buffer size.

    This function explores all permutations of daemons, merges them, and checks if they
    are valid (i.e., do not exceed the buffer size). It also identifies which daemons
    each merged sequence completes.

    Args:
        daemons: A list of daemons, where each daemon is a sequence of strings.
        buffer_size: The maximum allowed length for a merged sequence.

    Returns:
        A dictionary where keys are tuples of daemon indices and values are the shortest
        merged sequences that complete these daemons.
    """
    shortest_sequences = {}
    # Filter out daemons that are already larger than the buffer size
    valid_daemons = [(i, d) for i, d in enumerate(daemons) if len(d) <= buffer_size]
    daemon_indices, daemons = zip(*valid_daemons) if valid_daemons else ([], [])

    # Iterate through all possible lengths of daemon combinations
    for r in range(1, len(daemons) + 1):
        # Generate all permutations of daemon indices of length r
        for order in permutations(range(len(daemons)), r):
            # Start with the first daemon in the current permutation
            merged_sequence = daemons[order[0]]
            # Merge the rest of the daemons in the permutation
            for idx in order[1:]:
                merged_sequence = _overlap_merge(merged_sequence, daemons[idx])
                # If the merged sequence exceeds the buffer size, stop and try the next permutation
                if len(merged_sequence) > buffer_size:
                    break
            else:  # This block executes if the for loop completes without a break
                # Identify all daemons covered by the merged sequence
                covered_daemons = tuple(
                    sorted(
                        [
                            daemon_indices[i]
                            for i, d in enumerate(daemons)
                            if _contains_subsequence(merged_sequence, d)
                        ]
                    )
                )

                if covered_daemons:
                    # If we found a new combination of covered daemons or a shorter
                    # sequence for an existing one
                    if covered_daemons not in shortest_sequences or len(
                        merged_sequence
                    ) < len(shortest_sequences[covered_daemons]):
                        shortest_sequences[covered_daemons] = merged_sequence

    return shortest_sequences
