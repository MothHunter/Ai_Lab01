import numpy
import time
from queue import PriorityQueue

from generator import *


# class for nodes in the search-tree
class Node:
    def __init__(self, g, h, puzzle_state, parent_node):
        self.g = g  # cost (number of moves) accumulated to reach this node
        self.h = h  # estimation of cost to reach the goal state from this node
        self.puzzle_state = puzzle_state    # current state of the puzzle
        self.parent_node = parent_node      # parent node of this node (for backtracking)
        self.child_nodes = []               # child nodes of this node

    # "less than" function needed for comparison when sorting queue of nodes
    def __lt__(self, other):
        return get_cost(self) < get_cost(other)

    # "equal to" function needed for comparison when sorting queue of nodes
    def __eq__(self, other):
        return get_cost(self) == get_cost(other)


# global variables
goal_state = numpy.array([[0, 1, 2],
                          [3, 4, 5],
                          [6, 7, 8]])   # the state in which the puzzle counts as solved
n_nodes = 0                         # number of nodes created while solving a single puzzle
n_expanded = 0                      # number of expanded nodes while solving a single puzzle
hamming_time = numpy.zeros(100)     # array for storing hamming solve times
hamming_nodes = numpy.zeros(100)    # array for storing hamming node numbers
manhattan_time = numpy.zeros(100)   # array for storing manhattan solve times
manhattan_nodes = numpy.zeros(100)  # array for storing manhattan node numbers
counter = 0                         # counter for solved puzzles of this run


def expand_node(n, heuristics, sub_problem, node_queue, known_states):
    # the "global" keyword tells the function to use the global variable of this name
    global goal_state
    global n_nodes
    global n_expanded
    n_expanded += 1
    p0 = get_position(n.puzzle_state, 0)
    if validate_move(n, "up"):
        n_nodes += 1
        new_state = numpy.copy(n.puzzle_state)
        new_state[p0[0]][p0[1]] = new_state[p0[0]-1][p0[1]]
        new_state[p0[0] - 1][p0[1]] = 0
        if known_states.get(hash_puzzle(new_state)) is None:
            new_node = Node(n.g + 1, heuristics(new_state, goal_state, sub_problem), "up", new_state, n)
            node_queue.put(new_node)
            n.child_nodes.append(new_node)
            known_states[hash_puzzle(new_state)] = True
    if validate_move(n, "down"):
        n_nodes += 1
        new_state = numpy.copy(n.puzzle_state)
        new_state[p0[0]][p0[1]] = new_state[p0[0]+1][p0[1]]
        new_state[p0[0] + 1][p0[1]] = 0
        if known_states.get(hash_puzzle(new_state)) is None:
            new_node = Node(n.g + 1, heuristics(new_state, goal_state, sub_problem), "down", new_state, n)
            node_queue.put(new_node)
            n.child_nodes.append(new_node)
            known_states[hash_puzzle(new_state)] = True
    if validate_move(n, "right"):
        n_nodes += 1
        new_state = numpy.copy(n.puzzle_state)
        new_state[p0[0]][p0[1]] = new_state[p0[0]][p0[1]+1]
        new_state[p0[0]][p0[1] + 1] = 0
        if known_states.get(hash_puzzle(new_state)) is None:
            new_node = Node(n.g + 1, heuristics(new_state, goal_state, sub_problem), "right", new_state, n)
            node_queue.put(new_node)
            n.child_nodes.append(new_node)
            known_states[hash_puzzle(new_state)] = True
    if validate_move(n, "left"):
        n_nodes += 1
        new_state = numpy.copy(n.puzzle_state)
        new_state[p0[0]][p0[1]] = new_state[p0[0]][p0[1]-1]
        new_state[p0[0]][p0[1] - 1] = 0
        if known_states.get(hash_puzzle(new_state)) is None:
            new_node = Node(n.g + 1, heuristics(new_state, goal_state, sub_problem), "left", new_state, n)
            node_queue.put(new_node)
            n.child_nodes.append(new_node)
            known_states[hash_puzzle(new_state)] = True


def validate_solvable(start_array):
    # puzzle is solvable if number of inversions is even
    # an inversion is when a number is smaller than a previous number, when reading the array
    # from top to bottom and left to right (the empty tile 0 is not counted)
    inversions = 0

    # first, we convert the 2d array to a 1d array, excluding 0
    start_1d = []
    for r in range(0, 3):
        for c in range(0, 3):
            if start_array[r][c] != 0:
                start_1d.append(start_array[r][c])

    # second, we go through the 1d array and compare every number (i) to all following numbers (j)
    for i in range(0, 8):
        for j in range(i+1, 8):
            if start_1d[i] > start_1d[j]:
                # if the following number is smaller, we have an inversion
                inversions += 1

    # check if number of inversions is odd (unsolvable) or even (solvable)
    if inversions % 2 != 0:
        return False
    else:
        return True


def validate_move(node, direction):
    # check for errors in direction encoding
    if direction != "up" and direction != "right" and direction != "down" and direction != "left":
        print("invalid direction")
        return False
    # check for errors in previous_direction encoding
    if (node.previous_move != "up" and node.previous_move != "right" and node.previous_move != "down" and
            node.previous_move != "left" and node.previous_move != "none"):
        print("invalid previous_direction")
        return False
    # get column and row of the empty tile, to check in which direction we can move it
    row_of_0 = 0
    column_of_0 = 0
    for r in range(0, 3):
        for c in range(0, 3):
            if node.puzzle_state[r][c] == 0:
                row_of_0 = r
                column_of_0 = c
                break
    # check if move is possible
    if direction == "up" and row_of_0 > 0 and node.previous_move != "down":
        # wir sind nicht in der obersten Zeile und sind davor nicht nach unten gegangen => "up" ist möglich
        return True
    if direction == "right" and column_of_0 < 2 and node.previous_move != "left":
        return True
    if direction == "down" and row_of_0 < 2 and node.previous_move != "up":
        return True
    if direction == "left" and column_of_0 > 0 and node.previous_move != "right":
        return True
    else:
        return False


# calculate the hamming distance
# if sub_problem is true, only the lower row of the puzzle is considered
# parameters:
# - current_array (3x3 int numpy array): current state of the puzzle
# - goal_array (3x3 int numpy array): solved state of the puzzle
# - sub_problem (boolean): True = only solve lower row; False = solve whole puzzle
# return value (int): distance
def get_hamming(start_array, goal_array, sub_problem):
    difference = 0
    if sub_problem:
        difference = 6
        for c in range(0, 3):
            if start_array[2][c] != goal_array[2][c]:
                difference += 1
    else:
        for r in range(0, 3):
            for c in range(0, 3):
                if start_array[r][c] != goal_array[r][c]:
                    difference += 1
    return difference


# calculate manhattan distance
def get_manhattan(start_array, goal_array, sub_problem):
    distance = 0
    if sub_problem:
        distance = 19
        for c in range(0, 3):
            position_in_goal = get_position(goal_array, start_array[2][c])
            distance += abs(2 - position_in_goal[0])
            distance += abs(c - position_in_goal[1])
    else:
        for r in range(0, 3):
            for c in range(0, 3):
                position_in_goal = get_position(goal_array, start_array[r][c])
                distance += abs(r - position_in_goal[0])
                distance += abs(c - position_in_goal[1])
    return distance


def hash_puzzle(p):
    hash = (p[0][0] * 100000000 + p[0][1] * 10000000 + p[0][2] * 1000000
            + p[1][0] * 100000 + p[1][1] * 10000 + p[1][2] * 1000
            + p[2][0] * 100 + p[2][1] * 10 + p[2][2])
    return hash


# find the position of a specific number in the array
def get_position(puzzle_array, number):
    for r in range(0, 3):
        for c in range(0, 3):
            if puzzle_array[r][c] == number:
                return [r, c]
    return False


def get_cost(node):
    return node.g + node.h


def solve_8puzzle(start_state, heuristics):
    current_node = Node(0, heuristics(start_state, goal_state, True), "none", start_state, None)
    node_queue = PriorityQueue()
    # node_queue.put(get_cost(current_node), current_node)
    known_states = {hash_puzzle(start_state): True}
    global n_nodes
    n_nodes = 0
    start_time = time.time()
    sub_problem_solved = False
    while current_node.h != 0:
        if sub_problem_solved:
            expand_node(current_node, heuristics, False, node_queue, known_states)
            current_node = node_queue.get()
        else:
            expand_node(current_node, heuristics, True, node_queue, known_states)
            current_node = node_queue.get()
            if (heuristics == get_hamming and current_node.h <= 6) or \
                    (heuristics == get_manhattan and current_node.h <= 19):
                sub_problem_solved = True

    end_time = time.time()
    if heuristics == get_hamming:
        global hamming_time
        hamming_time[counter] = end_time - start_time
        hamming_nodes[counter] = n_nodes
    elif heuristics == get_manhattan:
        global manhattan_time
        manhattan_time[counter] = end_time - start_time
        manhattan_nodes[counter] = n_nodes
    else:
        print("uh oh")


def solve100():
    global counter
    counter = 0
    while counter < 100:
        start_state = generate_puzzle()
        if validate_solvable(start_state):
            solve_8puzzle(start_state, get_hamming)
            solve_8puzzle(start_state, get_manhattan)
            counter += 1
            print(counter)


solve100()
print("hamming:")
print("avg. time: ", numpy.sum(hamming_time)/100)
print("avg. nodes: ", numpy.sum(hamming_nodes)/100)
print("manhattan:")
print("avg. time: ", numpy.sum(manhattan_time)/100)
print("avg. nodes: ", numpy.sum(manhattan_nodes)/100)

