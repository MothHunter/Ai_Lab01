global start
start = [[1, 4, 2],
         [0, 3, 5],
         [6, 7, 8]]

goal = [[0, 1, 2],
       [3, 4, 5],
       [6, 7, 8]]

def validate_solvable(start_array, goal_array):
    if get_hamming(start_array, goal_array) % 2 != 0:
        return False
    else:
        return True

def validate_move(current_array, direction, previous_move):
    if direction != "up" and direction != "right" and direction != "down" and direction != "left":
        print("invalid direction")
        return False
    if previous_move != "up" and previous_move != "right" and previous_move != "down" and previous_move != "left":
        print("invalid previous_direction")
        return False
    row_of_0 = 0 # variable muss einen Startwert haben
    column_of_0 = 0
    for r in range(0, 3):
        for c in range(0, 3):
            if current_array[r][c] == 0:
                row_of_0 = r
                column_of_0 = c
                break;
    if direction == "up" and row_of_0 > 0 and previous_move != "down":
        # wir sind nicht in der obersten Zeile und sind davor nicht nach unten gegangen => "up" ist möglich
        return True
    if direction == "right" and column_of_0 < 2 and previous_move != "left":
        return True
    if direction == "down" and row_of_0 < 2 and previous_move != "up":
        return True
    if direction == "left" and column_of_0 > 0 and previous_move != "right":
        return True
    else:
        return False

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


#def solve_8puzzle(start_array, goal_array):


if validate_solvable(start, goal) == False:
     print("puzzle is not solvable")
print(get_hamming(start, goal))
print(get_manhattan(start, goal))
