import Node_mod
from copy import deepcopy
from enum import Enum


class MoveDirection(Enum):
    UP = "UP"           # 0
    DOWN = "DOWN"       # 1
    LEFT = "LEFT"       # 2
    RIGHT = "RIGHT"     # 3


def state_to_tuple(state):
    arr = []
    for row in state:
        for val in row:
            arr.append(val)
    return tuple(arr)


def get__position_of_number(state, number):
    for i, row in enumerate(state):
        for ii, value in enumerate(row):
            if value == number:
                return i, ii


# https://math.stackexchange.com/questions/293527/how-to-check-if-a-8-puzzle-is-solvable
def check_solvable(state):
    n = len(state)
    inversions = 0
    inversion_is_odd = 0
    if n % 2 == 0:
        blank_row, blank_y = get__position_of_number(state, 0)
        if blank_row % 2 == 0:
            inversion_is_odd = 1
    flat_state = state_to_tuple(state)
    for i, val_i in enumerate(flat_state):
        for j in range(i+1, len(flat_state)):
            if flat_state[j] > val_i:
                inversions += 1
    return inversions % 2 == inversion_is_odd


def heuristic_distance(state, goal_state):
    ratio = 8 // 4
    distance = 0
    state_size = pow(len(state), 2)
    for i in range(state_size):
        x1, y1 = get__position_of_number(state, i)
        x2, y2 = get__position_of_number(goal_state, i)
        # not admissible
        distance += pow(x1 - x2, 2) + pow(y1 - y2, 2)
    return distance


def execute_move(curr_node, move):
    # curr_node = deepcopy(curr_node)
    x, y = get__position_of_number(curr_node.state, 0)
    new_state = deepcopy(curr_node.state)
    if move == MoveDirection.UP:
        new_state[x][y] = new_state[x + 1][y]
        new_state[x + 1][y] = 0
    if move == MoveDirection.DOWN:
        new_state[x][y] = new_state[x - 1][y]
        new_state[x - 1][y] = 0
    if move == MoveDirection.LEFT:
        new_state[x][y] = new_state[x][y + 1]
        new_state[x][y + 1] = 0
    if move == MoveDirection.RIGHT:
        new_state[x][y] = new_state[x][y - 1]
        new_state[x][y - 1] = 0
    return new_state
    # new_moves = curr_node.moves + (move,)
    # return Node.Node(new_state, new_moves)