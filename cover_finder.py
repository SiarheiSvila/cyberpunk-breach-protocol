from itertools import combinations
from typing import List, Dict, Tuple, Set

# A set of daemon indices, e.g., {0, 2, 3}
DaemonSet = Set[int]
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
