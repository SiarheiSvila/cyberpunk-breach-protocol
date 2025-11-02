from itertools import permutations


def all_merged_sequences(daemons: list[list[str]], buffer_size: int):
    """
    Generate all valid merged sequences (≤ buffer_size)
    and annotate which daemons each sequence completes.
    """

    def overlap_merge(seq1, seq2):
        """Merge two sequences with maximal suffix-prefix overlap."""
        max_overlap = 0
        for i in range(min(len(seq1), len(seq2)), 0, -1):
            if seq1[-i:] == seq2[:i]:
                max_overlap = i
                break
        return seq1 + seq2[max_overlap:]


    def contains_subsequence(sequence, subseq):
        """Return True if 'subseq' appears contiguously inside 'sequence'."""
        n, m = len(sequence), len(subseq)
        for i in range(n - m + 1):
            if sequence[i:i + m] == subseq:
                return True
        return False

    shortest_sequences = {}

    for r in range(1, len(daemons) + 1):
        for order in permutations(range(len(daemons)), r):
            merged = daemons[order[0]]
            for idx in order[1:]:
                merged = overlap_merge(merged, daemons[idx])
                if len(merged) > buffer_size:
                    break
            else:
                covered = tuple(sorted([i for i, d in enumerate(daemons) if contains_subsequence(merged, d)]))

                if covered:
                    if covered not in shortest_sequences or len(merged) < len(shortest_sequences[covered]):
                        shortest_sequences[covered] = merged

    return shortest_sequences
