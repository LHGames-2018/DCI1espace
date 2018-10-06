from helper import *
from queue import PriorityQueue
#from path_finding import *


class Node():
    def __init__(self, x, y):
        self.coords = (x, y)
        self.estimate = 0
        self.cost = 0

    def __gt__(self, other):
        return self.estimate > other.estimate

    def __eq__(self, other):
        return self.estimate == other.estimate

    def __cmp__(self, other):
        print("comparing")
        return cmp(self.estimate, other.estimate)

def manhattan(coord1, coord2):
    return abs(coord1[0]-coord2[0]) + abs(coord1[1]-coord2[1])

def normalize_tiles(gameMap):
    result = [['#' for _ in range(gameMap.xMax+1)] for _ in range(gameMap.yMax+1)]
    tiles = gameMap.tiles
    for row in tiles:
        for tile in row:
            coord = tile.Position
            if tile.TileContent == TileContent.Empty:
                result[coord.y][coord.x] = ' '
            if tile.TileContent == TileContent.Resource:
                result[coord.y][coord.x] = 'R'
            if tile.TileContent == TileContent.House:
                result[coord.y][coord.x] = ' '


    return result

def print_view(maze):
    output = ""
    for row in maze:
        for col in row:
            output += col
        output += '\n'
    print(output)

def reconstruct_path(maze, paths, node):
    result = []
    while paths[node] != None:
        prev = paths[node]
        move = (node[0]-prev[0], node[1]-prev[1])
        result.insert(0, move)
        node = prev
    
    return result

def solve_path(maze, start, goal):
    print_view(maze)
    costs = {start.coords: 0}
    paths = {start.coords: None}
    queue = PriorityQueue() 
    queue.put(start)

    print(start.coords, goal.coords)

    while not queue.empty():
        current_node = queue.get()
        #print(current_node.coords)

        #print(current_node.coords)
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
    return None #"Could not find a solution."

def cost(maze, node, neighbor):
    return 1

def cost_estimate(maze, node, goal):
    return manhattan(node.coords, goal.coords) 

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
        if maze[pos[1]][pos[0]] == ' ' or maze[pos[1]][pos[0]] == 'R':
            result.append(Node(pos[0], pos[1]))
    return result

def find_closest(pos, nodes):
    closest = None
    min_distance = 1000000
    for node in nodes:
        if manhattan(pos.coords, node.coords) < min_distance:
            closest = node
            min_distance = manhattan(pos.coords, node.coords)
    return closest


class Bot:
    def __init__(self):
        pass

    def go_home(self, gameMap):
        tiles = normalize_tiles(gameMap)
        pos = self.PlayerInfo.Position
        pos = Node(pos.x, pos.y)
        house = self.PlayerInfo.HouseLocation
        house = Node(house.x, house.y)
        path = solve_path(tiles, pos, house)
        if path != None:
            point = Point(path[0][0], path[0][1])
            return create_move_action(point)
        else:
            return create_move_action(Point(-1, 0))

    def before_turn(self, playerInfo):
        """
        Gets called before ExecuteTurn. This is where you get your bot's state.
            :param playerInfo: Your bot's current state.
        """
        self.PlayerInfo = playerInfo

    def execute_turn(self, gameMap, visiblePlayers):
        #return create_move_action(Point(0, 1))
        tiles = normalize_tiles(gameMap)
        pos = self.PlayerInfo.Position
        pos = Node(pos.x, pos.y)
        house = self.PlayerInfo.HouseLocation
        house = Node(house.x, house.y)
        
        print(self.PlayerInfo.UpgradeLevels)
        if pos.coords == house.coords:
            player = self.PlayerInfo

            #if player.player.TotalResources > 10000:
            pass
            #return create_
        if self.PlayerInfo.CarriedResources < 1000:
            ressources = self.get_ressources(gameMap.tiles)
            #print(ressources)
            #print(pos)
            #closest_res = find_closest(pos, ressources)
            #print(closest_res.coords)

            ressources.sort(key=lambda x: manhattan(pos.coords, x.coords))
            for i in range(len(ressources)):
                path = solve_path(tiles, pos, ressources[i])
                if path != None:
                    break
            if len(ressources) == 0 or path == None:
                return self.go_home(gameMap)

            print(self.PlayerInfo.CarriedResources)
            point = Point(path[0][0], path[0][1])
            print(path)
            if len(path) > 1:
                return create_move_action(point)
            else:
                return create_collect_action(point)
        else:
            return self.go_home(gameMap)
        #path = solve_path(tiles, pos, closest_res)
        #print(path)
        #print(solve_path(gameMap, pos, )
        """
        This is where you decide what action to take.
            :param gameMap: The gamemap.
            :param visiblePlayers:  The list of visible players.
        """

        # Write your bot here. Use functions from aiHelper to instantiate your actions.
        return create_move_action(Point(0, 1))

    def after_turn(self):
        """
        Gets called after executeTurn
        """
        pass



    def get_ressources(self, tiles):
        ressources = []
        for row_index, row in enumerate(tiles):
            for col_index, tile in enumerate(row):
                #print(tile.TileContent)
                if tile.TileContent == TileContent.Resource:
                    ressources.append(Node(tile.Position.x, tile.Position.y))
        return ressources