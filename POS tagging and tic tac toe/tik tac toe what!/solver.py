#!/usr/local/bin/python3
# solver.py : solve the game
#
# Code by: singarju-vvaradh
#
# Based on skeleton code for CSCI-B551
#

import sys
import time
import random
from typing import Union, List, Tuple


def parse_board_string_to_grid(board: str, n: int) -> list[list[str]]:
    return [[k for k in board[i:i + n]] for i in range(0, len(board), n)]

def parse_board_grid_to_string(board: list[list[str]]) -> str:
    return "".join("".join(row) for row in board)

def return_empty_positions(board: list[list[str]]) -> list[tuple[int, int]]:
    return [(i, j) for i in range(len(board)) for j in range(len(board[i])) if board[i][j] == '.']


def is_finish_state(board: list[list[str]], n: int, m: int, length: int = 3) -> bool:
    """Check if the board is in a finish state (has a line of X's).
    
    Args:
        board (list[list[str]]): The game board as a 2D list
        n (int): Number of rows in the board
        m (int): Number of columns in the board
        length (int): Length of line needed to win (default 3)
    
    Returns:
        bool: True if board is in finish state, False otherwise
    """
    
    # Check rows
    for i in range(n):
        for j in range(m - length + 1):
            if all(board[i][j+k] == 'x' for k in range(length)):
                return True
    
    # Check columns
    for i in range(n - length + 1):
        for j in range(m):
            if all(board[i+k][j] == 'x' for k in range(length)):
                return True
    
    # Check diagonals 
    for i in range(n - length + 1):
        for j in range(m - length + 1):
            if all(board[i+k][j+k] == 'x' for k in range(length)):
                return True
    
    # Check diagonals
    for i in range(n - length + 1):
        for j in range(length - 1, m):
            if all(board[i+k][j-k] == 'x' for k in range(length)):
                return True
    
    return False


def check_line(board: List[List[str]], length: int) -> bool:
    """Check if a line of specified length exists."""
    # similar to is_finish_state() function
    n, m = len(board), len(board[0])
    
    # Check horizontal lines
    for i in range(n):
        for j in range(m - length + 1):
            if all(board[i][j+k] == 'x' for k in range(length)):
                return True
    
    # Check columns
    for i in range(n - length + 1):
        for j in range(m):
            if all(board[i+k][j] == 'x' for k in range(length)):
                return True
    
    # Check diagonals 
    for i in range(n - length + 1):
        for j in range(m - length + 1):
            if all(board[i+k][j+k] == 'x' for k in range(length)):
                return True
    
    # Check diagonals 
    for i in range(n - length + 1):
        for j in range(length - 1, m):
            if all(board[i+k][j-k] == 'x' for k in range(length)):
                return True
    
    return False

def count_lines_in_direction(board: List[List[str]], length: int, get_cell: callable) -> int:
    """
    Count potential lines in a given direction using a cell retrieval function.
    
    Args:
        board: 2D board
        length: Line length to check
        get_cell: Function to retrieve cell at (i, j) with offset
    
    Returns:
        Number of potential lines
    """
    n, m = len(board), len(board[0])
    line_count = 0
    
    for start_i in range(n):
        for start_j in range(m):
            # Check if we can form a line starting from this position
            try:
                cells = [get_cell(start_i, start_j, k) for k in range(length)]
                
                # Count X's in the potential line
                x_count = sum(1 for cell in cells if cell == 'x')
                
                # If there are X's but not a complete line, it's a potential line
                if 0 < x_count < length:
                    line_count += 1
            except IndexError:
                # If we go out of board bounds, skip this starting position
                continue
    
    return line_count

def find_best_move(board: List[List[str]], length: int) -> Tuple[int, int]:
    """Find the best move to minimize the risk of losing."""
    if isinstance(board, str):
        board = parse_board_string_to_grid(board, int(len(board)**0.5))
        
    empty_positions = return_empty_positions(board)
    
    # First, check if we can block any potential winning lines
    best_moves = []
    for i, j in empty_positions:
        # Try this position
        board[i][j] = 'x'
        
        # If this move creates a line, it's a losing move
        if check_line(board, length):
            board[i][j] = '.'
            continue
            
        # Count how many X's are adjacent to this position
        adjacent_xs = 0
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == 0 and dj == 0:
                    continue
                new_i, new_j = i + di, j + dj
                if (0 <= new_i < len(board) and 
                    0 <= new_j < len(board[0]) and 
                    board[new_i][new_j] == 'x'):
                    adjacent_xs += 1
        
        # Prefer moves that don't create too many adjacent X's
        if adjacent_xs <= 1:  # Allow at most one adjacent X
            best_moves.append((i, j))
        
        board[i][j] = '.'
    
    # If we found safe moves, choose randomly among them
    if best_moves:
        return random.choice(best_moves)
    
    # If no completely safe moves found, choose any valid move that doesn't create a line
    fallback_moves = []
    for i, j in empty_positions:
        board[i][j] = 'x'
        if not check_line(board, length):
            fallback_moves.append((i, j))
        board[i][j] = '.'
    
    if fallback_moves:
        return random.choice(fallback_moves)
    
    # If all else fails, choose any empty position
    return random.choice(empty_positions)

def solver(board: str, n: int, m: int, length: int ) -> List[List[str]]:
    """Solve the game and return the new board state."""
    assert set(board) in [{'.', 'x'}, {'.'}, {'x'}], "Invalid characters in board"
    assert len(board) == n * m, "Board size does not match n x m"
    if check_line(board, length):
        assert  "Game is already finished"
        return -1
    board_grid = parse_board_string_to_grid(board, m)
    
    # Find the best move
    i, j = find_best_move(board_grid, length)
    
    # Place X in the chosen position
    board_grid[i][j] = 'x'
    return board_grid


def print_board(board: Union[list[list[str]], str], n: int, m: int):
    """Prints the board in a human readable format.

    Args:
        board (Union[list[list[str]], str]): The board to be printed. 
        n (int): number of rows in the board. 
        m (int): number of columns in the board. 
    """
    if isinstance(board, str):
        assert len(board) == n * m, "Board size does not match n x m"
        board = parse_board_string_to_grid(board, m)
    
    for row in board:
        print("".join(row))
 

if __name__ == "__main__":
    board_string = sys.argv[1]
    n = int(sys.argv[2])
    m = int(sys.argv[3])
    length = int(sys.argv[4])  # Corrected index
    
    # Convert board to grid for is_finish_state check
    board_grid = parse_board_string_to_grid(board_string, m)
    
    # Check if game is already finished (X has formed a line)
    if is_finish_state(board_grid, n, m, length):
        print("Game is already finished: X has formed a line")
        sys.exit(1)  # Exit with error code
    
    print("Starting from initial board:\n")
    print_board(board_string, n, m)
    print("\nDeciding the next step...\n")
    new_board = solver(board_string, n, m, length)
    print("Here's what we found:\n")
    print_board(new_board, n, m)