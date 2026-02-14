# for board parsing, validation, and helpers

def make_goal(n):
    vals = list(range(1, n*n)) + [0]
    goal = []
    i = 0
    for _ in range(n):
        goal.append(tuple(vals[i:i+n]))
        i += n
    return tuple(goal)

def is_goal(board):
    n = len(board)
    return board == make_goal(n)

# for printing the board
def board_to_string(board):
    return "\n".join(" ".join(str(x) for x in row) for row in board)

# convert row string to tuple
def parse_row(row, n):
    parts = row.strip().split()
    if len(parts) != n:
        raise ValueError(f"Row must have {n} numbers exactly, separated by spaces.")
    return (tuple(int(x) for x in parts))

# convert n row strings to tuple of tuples
def parse_board(rows, n):
    if len(rows) != n:
        raise ValueError(f"Board must have {n} rows exactly.")

    boardRows = [parse_row(rows[i], n) for i in range(n)]
    board = tuple(boardRows)

    # check for validity of the board
    nums = []
    for r in board:
        nums.extend(r)

    if sorted(nums) != list(range(n*n)):
        raise ValueError(f"Board must contain all numbers 0-{n*n-1} exactly once.")
    
    return board

def find_blank(board):
    n = len(board)
    for r in range(n):
        for c in range(n):
            if board[r][c] == 0:
                return (r, c)
    raise ValueError("Board does not contain a blank space.")

# return new board with two tiles swapped
def swap(board, r1, c1, r2, c2):
    grid = [list(row) for row in board] # temp copy
    grid[r1][c1], grid[r2][c2] = grid[r2][c2], grid[r1][c1]
    return tuple(tuple(row) for row in grid)

# generate valid boards from one move
def expand(board):
    n = len(board)
    r, c = find_blank(board)
    neighbors = []

    #can go up, down, left, right
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dr, dc in moves:
        nr, nc = r + dr, c + dc
        if 0 <= nr < n and 0 <= nc < n:
            neighbors.append(swap(board, r, c, nr, nc))
    return neighbors


# ============= HEURISTICS ==========

# misplaced tiles - count number of tiles in the wrong position
def misplaced_tiles(board):
    n = len(board)
    goal = make_goal(n)
    
    count = 0
    for r in range(n):
        for c in range(n):
            val = board[r][c]
            if val != 0 and val != goal[r][c]:
                count += 1
    return count


#helper for manhattan distance - returns dict of values to their goal positions
def goal_positions(n):
    goal = make_goal(n)
    pos = {}
    for r in range(n):
        for c in range(n):
            pos[goal[r][c]] = (r, c)
    return pos

# manhattan distance - sum of distances from each tile to its goal positions
def manhattan(board):
    n = len(board)
    pos = goal_positions(n)

    total = 0
    for r in range(n):
        for c in range(n):
            val = board[r][c]
            if val == 0:
                continue
            goalR, goalC = pos[val]
            total += abs(r - goalR) + abs(c - goalC)
    return total

