
def find_sequence_path(matrix: list[list[str]], sequence: list[str], buffer_size: int):
    """
    Find a valid traversal path through the matrix for a given sequence.

    This function searches for a contiguous appearance of the sequence in the matrix,
    respecting the Cyberpunk 2077 breaching protocol rules (alternating row/column moves).

    Args:
        matrix: The grid of characters to search through.
        sequence: The sequence of characters to find.
        buffer_size: The maximum length of the traversal path.

    Returns:
        A list of (row, col) tuples representing the path of the sequence if found,
        otherwise an empty list.
    """
    n_rows, n_cols = len(matrix), len(matrix[0])
    target_len = len(sequence)

    # The stack will store tuples of:
    # (current_row, current_col, current_mode, visited_nodes, current_path, collected_tokens)
    stack = []

    # Initialize the search from all possible starting points in the first row
    for c in range(n_cols):
        start_node = (0, c)
        stack.append(
            (
                start_node[0],
                start_node[1],
                "col",  # Initial mode is to move to a different column
                {start_node},
                [start_node],
                [matrix[start_node[0]][start_node[1]]],
            )
        )

    while stack:
        r, c, mode, visited, path, tokens = stack.pop()

        # Check if the collected tokens contain the sequence
        if len(tokens) >= target_len and tokens[-target_len:] == sequence:
            return path[-target_len:]

        # Stop exploring this path if the buffer is full
        if len(path) >= buffer_size:
            continue

        # Explore next possible moves based on the current mode
        if mode == "col":
            # Move vertically to a different row in the same column
            for nr in range(n_rows):
                if nr != r and (nr, c) not in visited:
                    new_visited = visited | {(nr, c)}
                    new_path = path + [(nr, c)]
                    new_tokens = tokens + [matrix[nr][c]]
                    stack.append((nr, c, "row", new_visited, new_path, new_tokens))
        else:  # mode == "row"
            # Move horizontally to a different column in the same row
            for nc in range(n_cols):
                if nc != c and (r, nc) not in visited:
                    new_visited = visited | {(r, nc)}
                    new_path = path + [(r, nc)]
                    new_tokens = tokens + [matrix[r][nc]]
                    stack.append((r, nc, "col", new_visited, new_path, new_tokens))

    return []  # Return an empty list if no valid path is found
