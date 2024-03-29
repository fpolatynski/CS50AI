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
    number_x = 0
    number_o = 0
    for x in board:
        for y in x:
            if y == X:
                number_x += 1
            elif y == O:
                number_o += 1
    if number_o + number_x == 9:
        return None
    elif number_o < number_x:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    ans = set()
    for i, x in enumerate(board):
        for j, y in enumerate(x):
            if y is None:
                ans.add((i, j))
    return ans


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise ValueError
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows
    for x in board:
        if x[0] == x[1] and x[1] == x[2]:
            if x[0] != EMPTY:
                return x[0]
    # Check columns
    for i in range(len(board)):
        if board[0][i] == board[1][i] and board[1][i] == board[2][i]:
            if board[0][i] != EMPTY:
                return board[0][i]
    # Check diagonals
    if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        if board[1][1] != EMPTY:
            return board[1][1]
    if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        if board[1][1] != EMPTY:
            return board[1][1]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # If winning position
    if winner(board):
        return True
    # If actions able
    if len(actions(board)):
        return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    ans = winner(board)
    if ans == X:
        return 1
    elif ans == O:
        return -1
    else:
        return 0


def maxval(state):
    # if terminal state
    if terminal(state):
        return utility(state)
    else:
        # Find maximal value of possible moves
        temp = [-2]
        for a in actions(state):
            temp.append(minval(result(state, a)))
        return max(temp)


def minval(state):
    if terminal(state):
        return utility(state)
    else:
        temp = [2]
        for a in actions(state):
            temp.append(maxval(result(state, a)))
        return min(temp)


def minimax(board):
    print("MINIMAX")
    """
    Returns the optimal action for the current player on the board.
    """
    best_action = None
    if terminal(board):
        return None
    elif player(board) == X:
        best_action_value = -2
        for a in actions(board):
            temp = minval(result(board, a))
            if best_action_value < temp:
                best_action = a
                best_action_value = temp
    elif player(board) == O:
        best_action_value = 2
        for a in actions(board):
            temp = maxval(result(board, a))
            if best_action_value > temp:
                best_action = a
                best_action_value = temp
    return best_action


