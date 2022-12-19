global start
start = [[1, 4, 2],
         [0, 3, 5],
         [6, 7, 8]]

goal = [[0, 1, 2],
       [3, 4, 5],
       [6, 7, 8]]


def get_hamming(start_array, goal_array):
    difference = 0
    for r in range(0, 3):
        for c in range(0, 3):
            if start_array[r][c] != goal_array[r][c]:
                difference += 1
    return difference


def get_position(puzzle_array, zahl):
    for r in range(0, 3):
        for c in range(0, 3):
            if puzzle_array[r][c] == zahl:
                return [r, c]
    return False


def get_manhattan(start_array, goal_array):
    distance = 0
    for r in range(0, 3):
        for c in range(0, 3):
            position_in_goal = get_position(goal_array, start_array[r][c])
            distance += abs(r - position_in_goal[0])
            distance += abs(c - position_in_goal[1])
            print(start[r][c], position_in_goal)
    return distance


print(get_hamming(start, goal))
print(get_manhattan(start, goal))
