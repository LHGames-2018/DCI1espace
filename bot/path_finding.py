from queue import Queue

class Node():
    def __init__(self, x, y):
        self.coords = (x, y)
        self.estimate = 0
        self.cost = 0

    def __cmp__(self, other):
        return cmp(self.estimate, other.estimate)

def solve(maze, start, goal):
    costs = {start.coords: 0}
    paths = {start.coords: None}
    queue = PriorityQueue() 
    queue.put(start)

    while not queue.empty():
        current_node = queue.get()

        if current_node.coords == goal.coords:
            return reconstruct_path(maze, paths, current_node.coords)
        
        neighbors = get_neighbors(maze, current_node)
        for neighbor in neighbors:
            neighbor.cost = current_node.cost + cost(maze, current_node, neighbor)
            neighbor.estimate = neighbor.cost + cost_estimate(maze, neighbor, goal)
            if neighbor.coords not in costs or costs[neighbor.coords] > neighbor.cost:
                paths[neighbor.coords] = current_node.coords
                queue.put(neighbor)
                costs[neighbor.coords] = neighbor.cost
    return "Could not find a solution."

def cost(maze, node, neighbor):
    return 1

def cost_estimate(maze, node, goal):
    return abs(node.coords[0] - goal.coords[0]) + abs(node.coords[1] - goal.coords[1])

def get_neighbors(maze, node):
    result = []
    left  = (node.coords[0]-1, node.coords[1])
    up    = (node.coords[0], node.coords[1]-1)
    right = (node.coords[0]+1, node.coords[1])
    down  = (node.coords[0], node.coords[1]+1)
    positions = [up, right, down, left]

    for pos in positions:
        if pos[0] < 0 or pos[1] < 0:
            continue
        if maze[pos[1]][pos[0]] == ' ':
            result.append(Node(pos[0], pos[1]))
    return result