"""
This module provides functionality to find a sequence of tokens within a 2D matrix,
following specific traversal rules inspired by the Cyberpunk game's hacking minigame.
"""

def find_sequence_path(matrix: list[list[str]], sequence: list[str], buffer_size: int):
    """
    Finds a valid traversal path in a matrix for a given sequence.

    The traversal must follow these rules:
    1. The path is a sequence of coordinates (row, col).
    2. Moves alternate between horizontal and vertical (e.g., from (r1, c1) to (r1, c2)
       is a horizontal move, the next must be to (r2, c2)).
    3. A coordinate cannot be visited more than once in a single path.
    4. The total path length cannot exceed the buffer_size.

    The function searches for a path where the given `sequence` appears as a
    contiguous subsequence of the tokens collected along the path.

    Args:
        matrix: A 2D list of strings representing the grid of tokens.
        sequence: A list of strings representing the target sequence to find.
        buffer_size: An integer representing the maximum allowed length of the path.

    Returns:
        A list of (row, col) tuples representing the path segment that matches
        the sequence if found; otherwise, an empty list.
    """
    n_rows, n_cols = len(matrix), len(matrix[0])
    target_len = len(sequence)

    def dfs(r, c, mode, visited, path, tokens):
        # Base case: Check if the end of the current tokens matches the sequence
        if len(tokens) >= target_len and tokens[-target_len:] == sequence:
            return path[-target_len:]

        # Constraint: Stop if the path exceeds the buffer size
        if len(path) >= buffer_size:
            return None

        # Recursive step: Explore the next possible moves
        if mode == "col":
            # Vertical move: stay in the same column `c`, move to a new row `nr`
            next_mode = "row"
            for nr in range(n_rows):
                if nr != r and (nr, c) not in visited:
                    res = dfs(nr, c, next_mode, visited | {(nr, c)},
                              path + [(nr, c)], tokens + [matrix[nr][c]])
                    if res:
                        return res
        else:  # mode == "row"
            # Horizontal move: stay in the same row `r`, move to a new col `nc`
            next_mode = "col"
            for nc in range(n_cols):
                if nc != c and (r, nc) not in visited:
                    res = dfs(r, nc, next_mode, visited | {(r, nc)},
                              path + [(r, nc)], tokens + [matrix[r][nc]])
                    if res:
                        return res
        return None

    # Main loop: Try all cells as potential starting points for the path
    for r_start in range(n_rows):
        for c_start in range(n_cols):
            start_token = matrix[r_start][c_start]
            initial_path = [(r_start, c_start)]
            initial_tokens = [start_token]
            initial_visited = {(r_start, c_start)}

            # A path can start with either a vertical or horizontal move.
            # We initiate DFS for both possibilities from each starting cell.

            # Try starting with a vertical move
            if (res := dfs(r_start, c_start, "col", initial_visited, initial_path, initial_tokens)):
                return res

            # Try starting with a horizontal move
            if (res := dfs(r_start, c_start, "row", initial_visited, initial_path, initial_tokens)):
                return res

    return []  # Return empty list if no path is found
