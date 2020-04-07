"""
Tic Tac Toe Player
"""

import math
import copy
from itertools import chain

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
    # check rows for winner
    for row in board:
        if len(set(row)) == 1:
            return X if X in row else O
    # check columns
    for n in range(0,3):
        col = [row[n] for row in board]
        if len(set(col)) == 1:
            return X if X in row else O
    # check first diagonal for winner
    d1 = [board[el][el] for el in range(0,3)]
    if len(set(d1)) == 1:
        return X if X in d1 else O
    # check second diagonal for winner
    temp_board = board.reverse()
    d2 = [temp_board[el][el] for el in range(0,3)]
    if len(set(d2)) == 1:
        return X if X in d2 else O


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if EMPTY in list(chain(board)):
        return False
    else:
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board) == True:
        if winner(board) == X:
            return 1
        elif winner(board) == O:
            return -1
        else:
            return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    else:
        player = player(board)
        actions = actions(board)
        action_results = [(action, result(board, action))for action in actions]
        if player == X:
            v = max_value(board)
            for pair in action_results:
                if v == max_value(pair[1]):
                    return pair[0]
            return action
        else:
            v = min_value(board)
            for pair in action_results:
                if v == min_value(pair[1]):
                    return pair[0]


def max_value(board):
    if terminal(board):
        return utility(board)
    v = -float("inf")
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board):
    if terminal(board):
        return utility(board)
    v = float("inf")
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v