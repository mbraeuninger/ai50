from tictactoe import terminal

X = "X"
O = "O"
EMPTY = None

board = [[X, EMPTY, EMPTY],
            [EMPTY, X, EMPTY],
            [EMPTY, EMPTY, X]]
print(terminal(board))
print(board)
print(list(reversed(board)))