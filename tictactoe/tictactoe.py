"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    list_board = [field for row in board for field in row]
    return X if list_board.count(EMPTY) % 2 != 0 else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for row in enumerate(board):
        if EMPTY in row[1]:  # if there are no EMPTY values left we can skip
            for field in enumerate(row):
                if field[1] == EMPTY:
                    actions.add((row[0],field[0]))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # create a deepcopy of the board
    copy.deepcopy(board)
    # get the player whose turn it is
    player = player(board)
    # change the field that is being played
    if board[action[0]][action[1]] == EMPTY:
        board[action[0]][action[1]] = player
    else:
        raise Exception("Invalid move")
    return board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check if row is identical
    for row in board:
        if len(set(row)) == 1:
            return X if X in row else O
    # check if column is identical
    for n in range(0,3):
        col = [row[n] for row in board]
        if len(set(col)) == 1:
            return X if X in row else O
    # check if diagonal is identical
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
