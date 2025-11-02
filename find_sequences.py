"""
This module provides functions for generating all possible merged sequences
from a list of daemon sequences, respecting a maximum buffer size. It identifies
which daemons are covered by each generated sequence.
"""

from itertools import permutations
from typing import List, Tuple, Dict

def _overlap_merge(seq1: List[str], seq2: List[str]) -> List[str]:
    """
    Merges two sequences with the maximum possible suffix-prefix overlap.

    For example, merging ["A", "B", "C"] and ["B", "C", "D"] would result in
    ["A", "B", "C", "D"] with an overlap of "B", "C".
    """
    max_overlap = 0
    for i in range(1, min(len(seq1), len(seq2)) + 1):
        if seq1[-i:] == seq2[:i]:
            max_overlap = i
    return seq1 + seq2[max_overlap:]

def _contains_subsequence(sequence: List[str], subseq: List[str]) -> bool:
    """
    Checks if `subseq` appears as a contiguous subsequence within `sequence`.
    """
    n, m = len(sequence), len(subseq)
    for i in range(n - m + 1):
        if sequence[i:i + m] == subseq:
            return True
    return False

def get_all_merged_sequences(daemons: List[List[str]], buffer_size: int) -> Dict[Tuple[int, ...], List[str]]:
    """
    Generates all valid merged sequences from a list of daemons that are
    less than or equal to the specified buffer size.

    The function explores all permutations of daemons, from single daemons up to
    all daemons combined. For each permutation, it merges the sequences together,
    optimizing for overlap to create the shortest possible combined sequence.

    If a merged sequence is within the buffer size, it is stored with a key
    representing the daemons it covers.

    Args:
        daemons: A list of daemon sequences, where each daemon is a list of strings.
        buffer_size: The maximum allowed length for a merged sequence.

    Returns:
        A dictionary where keys are tuples of daemon indices covered, and values
        are the corresponding merged sequences.
    """
    num_daemons = len(daemons)
    merged_sequences = {}

    for r in range(1, num_daemons + 1):
        for daemon_indices in permutations(range(num_daemons), r):
            # Merge the sequences in the chosen order
            current_sequence = daemons[daemon_indices[0]]
            for i in range(1, len(daemon_indices)):
                current_sequence = _overlap_merge(current_sequence, daemons[daemon_indices[i]])
                if len(current_sequence) > buffer_size:
                    break

            # If the sequence is valid (within buffer size), check which daemons it covers
            if len(current_sequence) <= buffer_size:
                covered_daemons = tuple(sorted([
                    i for i, d in enumerate(daemons)
                    if _contains_subsequence(current_sequence, d)
                ]))

                # Store the sequence if it's the first or a shorter one for this set of daemons
                if covered_daemons not in merged_sequences or \
                   len(current_sequence) < len(merged_sequences[covered_daemons]):
                    merged_sequences[covered_daemons] = current_sequence

    return merged_sequences
