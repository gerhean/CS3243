import os
import sys
from IDSNode import IDSNode
from Util import execute_move, check_valid, opposite_move_dict
import time


class Puzzle(object):

    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.init_state = init_state
        self.goal_state = goal_state
        self.actions = list()

    def dls(self, depth_limit, init_node):
        # Initialization
        move_stack = []
        stack = [init_node]
        visited = {tuple(map(tuple, self.init_state)): 0}

        while stack:

            cur_node = stack.pop()
            while cur_node.depth < len(move_stack):
                move_stack.pop()

            prev_move = cur_node.move
            move_stack.append(prev_move)
            cur_depth = len(move_stack)

            # print visited

            # Testing purpose
            # print("Stack size: %d"%(len(stack)))
            # print("Current state:\n")
            # print(cur_node)

            if cur_node.state == self.goal_state:
                return move_stack[1: cur_depth]

            if cur_depth > depth_limit:
                continue

            moves = cur_node.get_possible_moves()
            if prev_move:
                moves.remove(opposite_move_dict[prev_move])

            for move in moves:
                next_state = execute_move(cur_node.state, move)
                next_space_tuple = tuple(map(tuple, next_state))
                if cur_depth > depth_limit:
                    continue

                if next_space_tuple in visited and visited[next_space_tuple] < cur_depth:
                    # print "already visited"
                    continue
                #  simple check which may or may not be efficient
                # self_loop = False
                # for node in stack:
                #     if node.depth > cur_depth - 12:
                #         break
                #     if node.state == next_state:
                #         self_loop = True
                #         break
                # if self_loop:
                #     continue

                next_node = IDSNode(next_state, move, cur_depth)
                stack.append(next_node)
                visited[next_space_tuple] = cur_depth + 1

        return ["UNSOLVABLE"]



    def solve(self):
        IDSNode.set_goal_state(goal_state)
        initial_node = IDSNode(init_state, None, 0)

        # Set the limit yourself
        limit = 30

        for x in range(1, limit):
            print("Running ids depth %d" %(x))
            result = self.dls(x, initial_node)

            if result == ["UNSOLVABLE"]:
                continue

            else:
                print("Solution found at depth %d"%(x))
                # return result
                print("Is valid?")
                print(check_valid(self.init_state, goal_state, result))
                return [e.value for e in result]

        return ["UNSOLVABLE"]

    # you may add more functions if you think is useful

if __name__ == "__main__":
    # do NOT modify below

    # argv[0] represents the name of the file that is being executed
    # argv[1] represents name of input file
    # argv[2] represents name of destination output file
    if len(sys.argv) != 3:
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        raise IOError("Input file not found!")

    lines = f.readlines()

    # n = num rows in input file
    n = len(lines)
    # max_num = n to the power of 2 - 1
    max_num = n ** 2 - 1

    # Instantiate a 2D list of size n x n
    init_state = [[0 for i in range(n)] for j in range(n)]
    goal_state = [[0 for i in range(n)] for j in range(n)]


    i,j = 0, 0
    for line in lines:
        for number in line.split(" "):
            if number == '':
                continue
            value = int(number , base = 10)
            if  0 <= value <= max_num:
                init_state[i][j] = value
                j += 1
                if j == n:
                    i += 1
                    j = 0

    for i in range(1, max_num + 1):
        goal_state[(i-1)//n][(i-1)%n] = i
    goal_state[n - 1][n - 1] = 0

    puzzle = Puzzle(init_state, goal_state)
    start_time = time.time()
    ans = puzzle.solve()
    elapsed_time = time.time() - start_time
    print(elapsed_time)

    with open(sys.argv[2], 'a') as f:
        for answer in ans:
            f.write(answer+'\n')






