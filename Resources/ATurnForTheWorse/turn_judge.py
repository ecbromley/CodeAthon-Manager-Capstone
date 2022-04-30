#!/usr/bin/python3
import sys

COURSE_CNT = 6

score = 0

if len(sys.argv) != 3:
    print('usage:   ' + sys.argv[0] + ' <course_file> <student_solution_file>')
    quit()

try:
    course_f = open(sys.argv[1], 'r')
    solutions = open(sys.argv[2], 'r').read().split('\n')
except:
    print(0)
    quit()

for i in range(COURSE_CNT):
    size = int(course_f.readline())  # how many locations per row and col
    ascii_size = (size * 2) - 1  # how many characters per row and col

    """
    Read in the course from the input file
    """
    row = col = None  # starting position of the unicycler
    course = [None] * ascii_size  # row dominant 2D version of course
    for r in range(ascii_size):
        course[r] = list(course_f.readline()[:-1])

        """
        Locate the starting row and column of the unicycler
        """
        if '@' in course[r]:
            row = r
            col = course[r].index('@')

    """
    Go to the next course if no solution is provided for this course.
    """
    if i >= len(solutions) or len(solutions[i]) == 0: continue

    # dir code   [ 0   1   2   3   4   5   6   7]
    row_offset = [-1, -1,  0, +1, +1, +1,  0, -1]
    col_offset = [ 0, +1, +1, +1,  0, -1, -1, -1]

    """
    Given a particular edge and direction, what will it be replaced with to
    show that edge cannot be traveled along again?
    """
    # dir codes   [0,4   1,5   2,6    3,7]
    safe_edges  = ['|', '/X',  '-', '\\X'] * 2  # edges repeat in second half
    replacement = [' ', ' \\', ' ',  ' /'] * 2  # edges repeat in second half

    prev_dir = int(solutions[i][0])  # ensure a first valid move scores

    for c in solutions[i]:
        """
        Go to the next course if the next character is not a direction.
        """
        if c not in '01234567': break

        dir = int(c)
        delta_r = row_offset[dir]
        delta_c = col_offset[dir]
        edge_row = row + delta_r
        edge_col = col + delta_c

        """
        Go to the next course if the move is invalid.
        """
        if edge_row not in range(ascii_size): break
        if edge_col not in range(ascii_size): break

        """
        Go to the next course if the move is invalid.
        """
        actual_edge = course[edge_row][edge_col]
        if actual_edge not in safe_edges[dir]: break

        """
        FABULOUS!  This was a valid move.  Update the edge so it can't be
        traveled again, update the unicycler's row and column, and adjust the
        score.
        """
        the_edge = safe_edges[dir].index(actual_edge)
        course[edge_row][edge_col] = replacement[dir][the_edge]

        row = edge_row + delta_r
        col = edge_col + delta_c

        if dir == prev_dir:
            score += 1

        prev_dir = dir

        """
        Just a sanity check for something that should never happen
        """
        if row not in range(ascii_size) or col not in range(ascii_size):
            print("DANGER:", row, col)
            quit()

print(score)
