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