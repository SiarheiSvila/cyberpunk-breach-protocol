# 🧩 Cyberpunk Breach Protocol Solver
https://www.cyberpunk-breach-protocol.com/

A Python simulation and solver for the Breach Protocol hacking minigame from Cyberpunk 2077.

Given a matrix of hex codes, a list of target daemons, and a limited buffer size — the program finds the optimal code sequence that uploads the maximum number of daemons following in-game movement rules.

## 🎮 Overview

In Cyberpunk 2077, the Breach Protocol minigame challenges the player to upload as many daemons as possible by selecting a sequence of codes from a grid.

Each daemon is represented by a sequence of hexadecimal codes (like `["E9", "55", "BD"]`). You must navigate the grid according to specific rules to build a buffer sequence that matches as many daemons as possible — in order — without exceeding the buffer limit.

This repository provides a Python implementation that simulates the grid movement and computes optimal or valid code sequences automatically.

## ⚙️ Game Rules

### 🧩 Inputs

You are given three key inputs:

#### 1. Matrix (Code Grid)
A 2D list of hexadecimal codes representing the game grid.

```python
matrix = [
    ['55', 'BD', 'E9', '1C', '55'],
    ['1C', '1C', '55', 'BD', 'E9'],
    ['BD', 'E9', '1C', '55', '1C'],
    ['E9', '55', '1C', 'BD', 'E9'],
    ['55', 'BD', 'E9', '1C', '55']
]
```

#### 2. Daemons (Target Sequences)
Each daemon is a list of codes that must appear as a contiguous subsequence in your buffer. The daemons must be matched in the order they are provided.

```python
daemons = [
    ["1C", "55", "E9"],  # Datamine_V1
    ["BD", "E9", "1C"],  # Datamine_V2
    ["55", "1C", "BD"]   # Datamine_V3
]
```

#### 3. Buffer Size
The maximum number of codes you can collect in your buffer sequence.

```python
buffer_size = 7
```

### 🧭 Movement Rules

To simulate Breach Protocol, the solver respects the same movement logic:

1. **Start Position**: You begin at any cell in the first row (row 0).

2. **Alternating Moves**: After the initial position, you must alternate between:
   - **Column Move**: Move down the current column to any row position
   - **Row Move**: Move across the current row to any column position

3. **Movement Pattern**: The pattern always alternates:
   ```
   Start (Row 0) → Column → Row → Column → Row → ...
   ```

4. **Collecting Codes**: Each cell you visit adds its hexadecimal code to your buffer sequence.

5. **Termination**: You stop when:
   - The buffer reaches the maximum size, or
   - You choose to stop early (before reaching the limit)

**Important Constraints:**
- You cannot visit the same cell twice
- You must follow the alternating movement pattern strictly
- The buffer sequence must be ≤ buffer_size in length

### 🎯 Objective

Find a sequence of codes that:

- Matches the maximum number of daemons (in the given order),
- Uses ≤ buffer_size codes,
- Follows the movement rules through the matrix.

A daemon is "matched" when its sequence appears as a contiguous subsequence in your buffer, in the exact order specified.

## 📋 Example

### Input

```python
matrix = [
    ['55', 'BD', 'E9', '1C', '55'],
    ['1C', '1C', '55', 'BD', 'E9'],
    ['BD', 'E9', '1C', '55', '1C'],
    ['E9', '55', '1C', 'BD', 'E9'],
    ['55', 'BD', 'E9', '1C', '55']
]

daemons = [
    ["1C", "55", "E9"],  # Datamine_V1
    ["BD", "E9", "1C"],  # Datamine_V2
    ["55", "1C", "BD"]   # Datamine_V3
]

buffer_size = 7
```

### Possible Solution

**Movement Path:**
```
Start at (0,4) → "55"    # Row 0, Column 4
    ↓ Column move
(2,4) → "1C"             # Row 2, Column 4
    → Row move
(2,0) → "BD"             # Row 2, Column 0
    ↓ Column move
(3,0) → "E9"             # Row 3, Column 0
    → Row move
(3,2) → "1C"             # Row 3, Column 2
    ↓ Column move
(1,2) → "55"             # Row 1, Column 2
    → Row move
(1,4) → "E9"             # Row 1, Column 4
```

**Buffer Sequence:**
```python
['55', '1C', 'BD', 'E9', '1C', '55', 'E9']
```

**Matched Daemons:**
- `["1C", "55", "E9"]` appears at positions [1, 5, 6] ✓
- `["BD", "E9", "1C"]` appears at positions [2, 3, 4] ✓
- `["55", "1C", "BD"]` does not appear as a contiguous subsequence ✗

This solution matches **2 out of 3 daemons** using all 7 buffer slots.

## 🧮 API Reference

### Problem Formulation

**Input:**
- `matrix`: `list[list[str]]` - A 2D grid of hexadecimal code strings
- `daemons`: `list[list[str]]` - List of daemon sequences to match (in order)
- `buffer_size`: `int` - Maximum length of the buffer sequence

**Output:**
The solver returns the optimal sequence(s) that maximize the number of matched daemons:

- **Basic Output**: `list[str]` - The optimal code sequence
- **Advanced Output**: `list[dict]` - List of sequences with metadata:
  - `sequence`: The code sequence
  - `path`: The matrix coordinates visited
  - `covers`: Which daemons are matched by this sequence

### Usage

```python
from main import find_matching_sequences

matrix = [['55', 'BD', 'E9', ...], ...]
daemons = [["1C", "55", "E9"], ["BD", "E9", "1C"], ...]
buffer_size = 7

find_matching_sequences(matrix, daemons, buffer_size)
```