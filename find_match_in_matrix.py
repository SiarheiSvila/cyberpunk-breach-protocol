def find_sequence_path(matrix: list[list[str]], sequence: list[str], buffer_size: int):
    """
    Find a valid traversal path through the matrix (following Cyberpunk rules)
    where the given sequence appears as a contiguous subsequence.

    Returns: list[(row, col)] if found, otherwise [].
    """

    n_rows, n_cols = len(matrix), len(matrix[0])
    target_len = len(sequence)

    def dfs(r, c, mode, visited, path, tokens):
        # Check if current token history contains the sequence
        if len(tokens) >= target_len:
            # Check last window of same length as sequence
            if tokens[-target_len:] == sequence:
                return path[-target_len:]  # return only the matching slice

        # Stop if buffer full
        if len(path) >= buffer_size:
            return None

        if mode == "col":
            # move vertically in same column
            for nr in range(n_rows):
                if nr != r and (nr, c) not in visited:
                    res = dfs(
                        nr, c, "row", visited | {(nr, c)},
                        path + [(nr, c)],
                        tokens + [matrix[nr][c]]
                    )
                    if res:
                        return res

        else:  # mode == "row"
            # move horizontally in same row
            for nc in range(n_cols):
                if nc != c and (r, nc) not in visited:
                    res = dfs(
                        r, nc, "col", visited | {(r, nc)},
                        path + [(r, nc)],
                        tokens + [matrix[r][nc]]
                    )
                    if res:
                        return res
        return None

    # Try all possible starting points in the first row
    for c in range(n_cols):
        start_token = matrix[0][c]
        res = dfs(
            0, c, "col",
            {(0, c)},
            [(0, c)],
            [start_token]
        )
        if res:
            return res

    return []  # no valid path found
