"""
This module provides a function to find a valid traversal path
for a given sequence within a matrix, following specific movement rules.
"""
from dataclasses import dataclass
from typing import List, Set, Tuple


@dataclass
class SearchState:
    """
    Represents the state of the search at a particular node.
    """
    r: int
    c: int
    mode: str
    visited: Set[Tuple[int, int]]
    path: List[Tuple[int, int]]
    tokens: List[str]


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

    stack: List[SearchState] = []

    # Initialize the search from all possible starting points in the first row
    for c in range(n_cols):
        start_node = (0, c)
        stack.append(
            SearchState(
                r=start_node[0],
                c=start_node[1],
                mode="col",
                visited={start_node},
                path=[start_node],
                tokens=[matrix[start_node[0]][start_node[1]]],
            )
        )

    while stack:
        state = stack.pop()

        # Check if the collected tokens contain the sequence
        if len(state.tokens) >= target_len and state.tokens[-target_len:] == sequence:
            return state.path[-target_len:]

        # Stop exploring this path if the buffer is full
        if len(state.path) >= buffer_size:
            continue

        # Explore next possible moves based on the current mode
        _explore_next_moves(stack, matrix, state, n_rows, n_cols)

    return []  # Return an empty list if no valid path is found


def _explore_next_moves(
    stack: List[SearchState],
    matrix: List[List[str]],
    state: SearchState,
    n_rows: int,
    n_cols: int,
):
    """
    Helper function to explore the next possible moves from the current state.
    """
    if state.mode == "col":
        # Move vertically to a different row in the same column
        for nr in range(n_rows):
            if nr != state.r and (nr, state.c) not in state.visited:
                new_visited = state.visited | {(nr, state.c)}
                new_path = state.path + [(nr, state.c)]
                new_tokens = state.tokens + [matrix[nr][state.c]]
                stack.append(
                    SearchState(nr, state.c, "row", new_visited, new_path, new_tokens)
                )
    else:  # mode == "row"
        # Move horizontally to a different column in the same row
        for nc in range(n_cols):
            if nc != state.c and (state.r, nc) not in state.visited:
                new_visited = state.visited | {(state.r, nc)}
                new_path = state.path + [(state.r, nc)]
                new_tokens = state.tokens + [matrix[state.r][nc]]
                stack.append(
                    SearchState(state.r, nc, "col", new_visited, new_path, new_tokens)
                )
