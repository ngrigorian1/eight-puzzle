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

    # temp testing
    print("Neighbors:\n")
    for nb in puzzle.expand(board):
        print(puzzle.board_to_string(nb))
        print("\n")

if __name__ == "__main__":
    main()