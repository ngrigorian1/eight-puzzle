# for basic user inputs and printing starter board

import puzzle
import search

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

    #testing
    print("\nSelect algorithm:")
    print("1. Uniform Cost Search")
    print("2. A* w/ Misplaced Tile heuristic")
    print("3. A* w/ Manhattan Distance heuristic")

    choice = input("Enter choice: ").strip()

    if choice == "1":
        result = search.uniform_cost_search(board)
    elif choice == "2":
        result = search.astar_misplaced(board)
    elif choice == "3":
        result = search.astar_manhattan(board)
    else:
        print("Invalid algorithm choice.")
        return

    if result == "failure":
        print("\nNo solution found.")
        return

    print("\nSolution found!")
    print("Solution depth:", result["solution_depth"])
    print("Nodes expanded:", result["nodes_expanded"])
    print("Max queue size:", result["max_queue_size"])

    # print solution path
    print("\nSolution path:\n")
    path = search.solution_path(result["goal_node"])
    for state in path:
        print(puzzle.board_to_string(state))
        print("\n")


if __name__ == "__main__":
    main()