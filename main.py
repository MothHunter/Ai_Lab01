import numpy

from generator import *
import numpy as np


class Node:
    def __init__(self, g, h, previous_move, puzzle_state, parent_node):
        self.g = g
        self.h = h
        # previous move is encoded as "up", "down", "left", "right"
        # for initial node use "none" as previous move
        # used to avoid cycling back and forth between two states
        self.previous_move = previous_move
        self.puzzle_state = puzzle_state
        self.parent_node = parent_node
        self.child_nodes = []


# global variables
goal_state = np.array([[0, 1, 2],
                       [3, 4, 5],
                       [6, 7, 8]])
n_nodes = 0     # number of nodes created
n_expanded = 0   # number of expanded nodes


def expand_node(n, heuristics, node_list):
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
        new_node = Node(n.g + 1, heuristics(new_state, goal_state), "up", new_state, n)
        node_list.append(new_node)
        n.child_nodes.append(new_node)
    if validate_move(n, "down"):
        n_nodes += 1
        new_state = numpy.copy(n.puzzle_state)
        new_state[p0[0]][p0[1]] = new_state[p0[0]+1][p0[1]]
        new_state[p0[0] + 1][p0[1]] = 0
        new_node = Node(n.g + 1, heuristics(new_state, goal_state), "down", new_state, n)
        node_list.append(new_node)
        n.child_nodes.append(new_node)
    if validate_move(n, "right"):
        n_nodes += 1
        new_state = numpy.copy(n.puzzle_state)
        new_state[p0[0]][p0[1]] = new_state[p0[0]][p0[1]+1]
        new_state[p0[0]][p0[1] + 1] = 0
        new_node = Node(n.g + 1, heuristics(new_state, goal_state), "right", new_state, n)
        node_list.append(new_node)
        n.child_nodes.append(new_node)
    if validate_move(n, "left"):
        n_nodes += 1
        new_state = numpy.copy(n.puzzle_state)
        new_state[p0[0]][p0[1]] = new_state[p0[0]][p0[1]-1]
        new_state[p0[0]][p0[1] - 1] = 0
        new_node = Node(n.g + 1, heuristics(new_state, goal_state), "left", new_state, n)
        node_list.append(new_node)
        n.child_nodes.append(new_node)


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
def get_hamming(start_array, goal_array):
    difference = 0
    for r in range(0, 3):
        for c in range(0, 3):
            if start_array[r][c] != goal_array[r][c]:
                difference += 1
    return difference


# calculate manhattan distance
def get_manhattan(start_array, goal_array):
    distance = 0
    for r in range(0, 3):
        for c in range(0, 3):
            position_in_goal = get_position(goal_array, start_array[r][c])
            distance += abs(r - position_in_goal[0])
            distance += abs(c - position_in_goal[1])
    return distance


# find the position of a specific number in the array
def get_position(puzzle_array, number):
    for r in range(0, 3):
        for c in range(0, 3):
            if puzzle_array[r][c] == number:
                return [r, c]
    return False




def get_cost(node):
    return node.g + node.h


def solve_8puzzle(current_node, goal_array, heuristics):
    node_list = [current_node, ]
    print("node list length: " + str(len(node_list)))
    while current_node.h != 0:
        expand_node(current_node, heuristics, node_list)
        node_list.remove(current_node)
        node_list.sort(key=get_cost)
        current_node = node_list[0]


def solve100(heuristics):
    counter = 0
    while counter < 100:
        start_state = generate_puzzle()
        if validate_solvable(start_state):
            start_node = Node(0, heuristics(start_state, goal_state), "none", start_state, None)
            solve_8puzzle(start_node, goal_state, heuristics)
            counter += 1
            print(counter)


solve100(get_hamming)
