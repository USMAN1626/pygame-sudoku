
from copy import deepcopy

def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None

def solve(board):
    """
    Core recursive solver, modifies board in-place.
    """
    empty = find_empty(board)
    if not empty:
        return True
    row, col = empty

    possible_nums = set(range(1, 10))

    # Rule One: Elimination
    for i in range(9):
        possible_nums.discard(board[row][i])
        possible_nums.discard(board[i][col])
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            possible_nums.discard(board[start_row + i][start_col + j])

    if len(possible_nums) == 1:
        board[row][col] = possible_nums.pop()
        if solve(board):
            return True
        board[row][col] = 0
        return False

    # Rule Two & Three (trying remaining candidates)
    for num in possible_nums:
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve(board):
                return True
            board[row][col] = 0

    return False

def get_solved_board(unsolved_board):
    """
    Given an unsolved board, return a **new solved board**.
    Input:
        unsolved_board: list of lists (9x9), 0 for empty
    Output:
        solved_board: list of lists (9x9), or None if unsolvable
    """
    board_copy = deepcopy(unsolved_board)
    if solve(board_copy):
        return board_copy
    else:
        return None 
