# general search for sliding puzzles

import heapq
import puzzle

class Problem:
    def __init__(self, initial_state):
        self.INITIAL_STATE = initial_state

    def GOAL_TEST(self, state):
        return puzzle.is_goal(state)
    
    def OPERATORS(self, state):
        return puzzle.expand(state)

class Node:
    def __init__(self, state, parent, g, h=0):
        self.STATE = state
        self.PARENT = parent
        self.g = g # cost so far
        self.h = h # heuristic value
        self.f = g + h # total cost

# ================= helpers ===================

def MAKE_NODE(state, parent, g, h):
    return Node(state, parent, g, h)

# 
def MAKE_QUEUE(node):
    nodes = []
    # heap items: (priority, tie, node)
    heapq.heappush(nodes, (node.f, 0, node))
    return nodes

def EMPTY(nodes):
    return len(nodes) == 0

def REMOVE_FRONT(nodes):
    _, _, node = heapq.heappop(nodes)
    return node

def EXPAND(node, operators):
    children = []
    for child_state in operators(node.STATE):
        child_node = MAKE_NODE(child_state, node, node.g + 1, 0)
        children.append(child_node)
    return children

# ================= queueing functions ===================

def UCS_QUEUE(nodes, children):
    for child in children:
        # skip if not better g
        old = UCS_QUEUE.best_g.get(child.STATE)
        if old is not None and child.g >= old:
            continue

        UCS_QUEUE.best_g[child.STATE] = child.g

        child.h = 0
        child.f = child.g  # UCS priority = g

        heapq.heappush(nodes, (child.f, UCS_QUEUE.tie, child))
        UCS_QUEUE.tie += 1

    return nodes

def ASTAR_MISPLACED_QUEUE(nodes, children):
    for child in children:
        # keep best-known path cost
        old = ASTAR_MISPLACED_QUEUE.best_g.get(child.STATE)
        if old is not None and child.g >= old:
            continue

        ASTAR_MISPLACED_QUEUE.best_g[child.STATE] = child.g

        child.h = puzzle.misplaced_tiles(child.STATE)
        child.f = child.g + child.h

        heapq.heappush(nodes, (child.f, ASTAR_MISPLACED_QUEUE.tie, child))
        ASTAR_MISPLACED_QUEUE.tie += 1

    return nodes


def ASTAR_MANHATTAN_QUEUE(nodes, children):
    for child in children:
        # keep best-known path cost
        old = ASTAR_MANHATTAN_QUEUE.best_g.get(child.STATE)
        if old is not None and child.g >= old:
            continue

        ASTAR_MANHATTAN_QUEUE.best_g[child.STATE] = child.g

        child.h = puzzle.manhattan(child.STATE)
        child.f = child.g + child.h

        heapq.heappush(nodes, (child.f, ASTAR_MANHATTAN_QUEUE.tie, child))
        ASTAR_MANHATTAN_QUEUE.tie += 1

    return nodes


def general_search(problem, QUEUEING_FUNCTION):
    start = MAKE_NODE(problem.INITIAL_STATE, None, 0, 0)
    nodes = MAKE_QUEUE(start)

    best_g = {}
    best_g[problem.INITIAL_STATE] = 0
    # shared best_g across queueing
    QUEUEING_FUNCTION.best_g = best_g

    nodes_expanded = 0
    max_queue_size = 1

    while True:
        if EMPTY(nodes):
            return "failure"

        if len(nodes) > max_queue_size:
            max_queue_size = len(nodes)

        node = REMOVE_FRONT(nodes)
        # if not the best known path to its state, skip 
        if node.g != QUEUEING_FUNCTION.best_g.get(node.STATE):
            continue
        nodes_expanded += 1

        if problem.GOAL_TEST(node.STATE):
            return {
                "goal_node": node,
                "solution_depth": node.g,
                "nodes_expanded": nodes_expanded,
                "max_queue_size": max_queue_size,
            }

        nodes = QUEUEING_FUNCTION(nodes, EXPAND(node, problem.OPERATORS))



# ================= utility ========
def solution_path(goal_node):
    path = []
    node = goal_node
    while node is not None:
        path.append(node.STATE)
        node = node.PARENT
    path.reverse()
    return path


# == wrappers ==
def uniform_cost_search(initial_board):
    problem = Problem(initial_board)
    UCS_QUEUE.tie = 1
    return general_search(problem, UCS_QUEUE)

def astar_misplaced(initial_board):
    problem = Problem(initial_board)
    ASTAR_MISPLACED_QUEUE.tie = 1
    return general_search(problem, ASTAR_MISPLACED_QUEUE)

def astar_manhattan(initial_board):
    problem = Problem(initial_board)
    ASTAR_MANHATTAN_QUEUE.tie = 1
    return general_search(problem, ASTAR_MANHATTAN_QUEUE)

