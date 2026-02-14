# for basic user inputs and printing starter board

import puzzle

def main():
    print("Welcome to the n-puzzle solver.")
    mode = input("Type 1 for a built-in puzzle (3x3), or 2 to enter your own.\n").strip()

    if mode == "1":
        board = (
            (1, 2, 3),
            (4, 5, 6),
            (7, 0, 8)
        )
    elif mode == "2":
        n = int(input("Enter the size of the puzzle (n): ").strip())
        print(f"Enter {n} rows, and use 0 for the blank space. Only seperate numbers by spaces.")
        rows = []
        for i in range(n):
            rows.append(input(f"Row {i+1}: ").strip())

        board = puzzle.parse_board(rows, n)
    else:
        print("Invalid choice.")
        return

    print("\nYour initial board is:\n")
    print(puzzle.board_to_string(board))

    # TEMP TESTING
    test_board = ((1, 2, 3), (4, 5, 6), (7, 0, 8))
    test2 = puzzle.make_goal(3)
    test3 = ((1,2,3,4),(5,6,7,8), (9,10,0,12),(13,14,11,15))
    print("Misplaced tiles:", puzzle.misplaced_tiles(test2)) # should be 0
    print("Manhattan distance:", puzzle.manhattan(test_board)) # should be 1
    print("Misplaced tiles:", puzzle.misplaced_tiles(test3)) # should be 2
    print("Manhattan distance:", puzzle.manhattan(test3)) # should be 2
    

if __name__ == "__main__":
    main()