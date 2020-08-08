"""
Tic Tac Toe Player
"""

import math
import copy
import random

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
    # initialize variables for the count of Xs and Os
    X_num = 0
    O_num = 0

    # increment the number of Xs and Os as game continues
    for row in board:
        for Box in row:
            if Box == X:
                X_num += 1
            elif Box == O:
                O_num += 1

    # return either X or O
    if X_num > O_num:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # set of possible actions
    actions_set = []

    for i in range(3):  # rows in the board (0, 1, 2)
        for j in range(3):  # boxs in rows (0, 1, 2)
            if board[i][j] == EMPTY:
                actions_set.append((i, j))
    return actions_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # if not valid action
    if action not in actions(board):
        raise Exception("Invalid action!")

    i, j = action
    turn = player(board)
    # make deepcopy of board and let current player make their move
    new_board = copy.deepcopy(board)
    new_board[i][j] = turn

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    wins = []

    # rows
    for i in range(3):
        wins.append(set([board[i][r] for r in range(3)])) # e.g. [0][0], [0][1], [0][2]

    # columns
    for i in range(3):
        wins.append(set([board[c][i] for c in range(3)])) # e.g. [0][0], [1][0], [2][0]

    # diagonals
    wins.append(set([board[i][i] for i in range(3)])) # [0][0], [1][1], [2][2]
    wins.append(set([board[i][2 - i] for i in range(3)])) # [0][2], [1][1], [2][0]

    #If X wins game, return X. If O wins game, return O. If no winner, return None
    for values in wins:
        if values == {X}:
            return X
        elif values == {O}:
            return O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    *If the game is over, either because someone has won the game or because all cells have been filled without anyone winning,
    the function should return True.
    *Otherwise, the function should return False if the game is still in progress.
    """
    if not actions(board) or winner(board) != None:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    W = winner(board)

    # if X won game -> utility of 1
    if W == X:
        return 1

    # if O won game -> utility of -1
    elif W == O:
        return -1

    # if tie -> utility of 0
    else:
        return 0


def MAX_value(board):
    """
    Takes state as input and returns output the maximizing value of the state.
    """
    # if game over, return winner
    if terminal(board):
        return utility(board)
    # initial value low as possible
    v = -math.inf
    # loop through possible actions and pick the maximum of the min player's scores
    for action in actions(board):
        v = max(v, MIN_value(result(board, action)))
    return v


def MIN_value(board):
    """
    Takes state as input and return output the  minimizing value of state.
    """
    # if game over, return winner
    if terminal(board):
        return utility(board)
    # initial value high as possible
    v = math.inf
    #loop through possible actions and pick minimum of max player's scores
    for action in actions(board):
        v = min(v, MAX_value(result(board, action)))
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    *The move returned should be the optimal action (i, j) that is one of the allowable actions on the board.
    *If multiple moves are equally optimal, any of those moves is acceptable.
    *If the board is a terminal board, the minimax function should return None.
    """
    #if game over, return None
    if terminal(board):
        return None

    # first move by AI
    if len(actions(board)) == 9:
        return (random.choice(actions(board)))

    #the max player (X) picks action which gives highest value from min player
    if player(board) == X:
        v = -math.inf
        result_action = None
        for action in actions(board):
            min_result = MIN_value(result(board, action))
            if min_result > v:
                v = min_result
                result_action = action

    #the min player (O) picks action which gives lowest value from max player
    if player(board) == O:
        v = math.inf
        result_action = None
        for action in actions(board):
            max_result = MAX_value(result(board, action))
            if max_result < v:
                v = max_result
                result_action = action

    return result_action