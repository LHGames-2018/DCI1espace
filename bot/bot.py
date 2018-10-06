from helper import *
import math
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

def manhattan(coord1, coord2):
    return abs(coord1[0]-coord2[0]) + abs(coord1[1]-coord2[1])

def normalize_tiles(gameMap, playerPos, housePos):
    tiles = gameMap.tiles
    max_x = 0
    max_y = 0
    for row in tiles:
        for tile in row:
            if tile.Position.x > max_x:
                max_x = tile.Position.x
            if tile.Position.y > max_y:
                max_y = tile.Position.y

    overflow_left = 0
    overflow_up = 0
    overflow_right = 0
    overflow_down = 0
    if playerPos.x - 10 < 0:
        overflow_left = abs(playerPos.x-10)
    if playerPos.y - 10 < 0:
        overflow_up = abs(playerPos.y-10)
    if playerPos.x + 10 > max_x:
        overflow_right = (playerPos.x+10) - max_x
    if playerPos.y + 10 > max_y:
        overflow_down  = (playerPos.y+10) - max_y

    result = [[' ' for _ in range(255)] for _ in range(255)]
    for row in tiles:
        for tile in row:
            coord = tile.Position
            #if coord.x > max_x - overflow_left:
            #    coord.x = 254 - (max_x - coord.x)
            #if coord.y > max_y - overflow_up:
            #    coord.y = 254 - (max_y - coord.y)

            #if coord.y < overflow_down:
            #    coord.y = max_y + coord.y + 1
            #if coord.x < overflow_right:
            #    coord.x = max_x + coord.x + 1

            if tile.TileContent == TileContent.Empty:
                result[coord.y][coord.x] = ' '
            if tile.TileContent == TileContent.Resource:
                result[coord.y][coord.x] = 'R'
            if tile.TileContent == TileContent.House:
                if housePos.x == coord.x and housePos.y == coord.y:
                    result[coord.y][coord.x] = ' '
                else:
                    result[coord.y][coord.x] = '#'
            if tile.TileContent == TileContent.Wall:
                result[coord.y][coord.x] = 'T'
            if tile.TileContent == TileContent.Lava:
                result[coord.y][coord.x] = '#'
            if tile.TileContent == TileContent.Player:
                result[coord.y][coord.x] = 'P'
            if tile.TileContent == TileContent.Shop:
                result[coord.y][coord.x] = 'S'
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
    #print_view(maze)
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
        
        neighbors = get_neighbors(maze, current_node, goal)
        for neighbor in neighbors:
            neighbor.cost = current_node.cost + cost(maze, current_node, neighbor)
            neighbor.estimate = neighbor.cost + cost_estimate(maze, neighbor, goal)
            if neighbor.coords not in costs or costs[neighbor.coords] > neighbor.cost:
                paths[neighbor.coords] = current_node.coords
                queue.put(neighbor)
                costs[neighbor.coords] = neighbor.cost
    return None

def cost(maze, node, neighbor):
    return 1

def cost_estimate(maze, node, goal):
    return manhattan(node.coords, goal.coords) 

def get_neighbors(maze, node, goal):
    result = []
    left  = (node.coords[0]-1, node.coords[1])
    up    = (node.coords[0], node.coords[1]-1)
    right = (node.coords[0]+1, node.coords[1])
    down  = (node.coords[0], node.coords[1]+1)
    Positions = [up, right, down, left]

    for pos in Positions:
        #if pos[0] < 0:
        #    pos[0] = 254
        #if pos[1] < 0:
        #    pos[1] = 254
        #if pos[0] >= 255:
        #    pos[0] = 0
        #if pos[1] >= 255:
        #    pos[1] = 0
        if pos == goal.coords or maze[pos[1]][pos[0]] == ' ' or maze[pos[1]][pos[0]] == 'T':
            result.append(Node(pos[0], pos[1]))
    return result

RESSOURCE_BY_BLOC = 1000 # guess
RESSOURCE_BY_PLAYER = 10000

class Bot:
    def __init__(self):
        self.peace = 0
        self.prev_score = 0
        pass

    def sortClosest(self, tiles, type):
        ressources = []
        for row_index, row in enumerate(tiles):
            for col_index, tile in enumerate(row):
                #print(tile.TileContent)
                if tile.TileContent == type:
                    ressources.append(Node(tile.Position.x, tile.Position.y))

        nodeOwnPos = Node(self.PlayerInfo.Position.x, self.PlayerInfo.Position.y)
        ressources.sort(key=lambda x: manhattan(nodeOwnPos.coords, x.coords))
        return ressources

    def evaluateRessource(self):
        return -math.inf
        closestRessource = self.sortClosest(self.gameMap.tiles, 4)

        for ressource in closestRessource:
            pos = Node(self.PlayerInfo.Position.x, self.PlayerInfo.Position.y)
            path = solve_path(self.gameMap._tiles, pos, ressource)
            if path != None:
                self.ressourcePath = path
                break
        if len(closestRessource) == 0:
            return -math.inf
        return RESSOURCE_BY_BLOC / len(path)

    def evaluatekill(self):
        closestplayer = self.sortClosest(self.gameMap.tiles, TileContent.Player)[1:]

        for player in closestplayer:
            pos = Node(self.PlayerInfo.Position.x, self.PlayerInfo.Position.y)
            path = solve_path(self.gameMap._tiles, pos, player)
            if path != None:
                self.killingPath = path
                break
        if len(closestplayer) == 0:
            print("wtf")
            return -math.inf
        print("test", len(path), RESSOURCE_BY_PLAYER / len(path))
        return RESSOURCE_BY_PLAYER / len(path)

    def evaluateUpgrade(self):
        return -math.inf, UpgradeType.AttackPower
        essentialItems = ["Sword", "Shield", "Backpack"]
        totalRessources = self.PlayerInfo.totalRessources
        level = self.PlayerInfo.getUpgradeLevel(self, self.PlayerInfo.CarryingCapacity)
        priority = -math.inf, None
        
        if(level <= 3):
            if level == 1 and totalRessources >= 10000:
                priority = math.inf, UpgradeType.CarryingCapacity
            if level == 2 and totalRessources >= 15000:
                priority = math.inf, UpgradeType.CarryingCapacity
            if level == 3 and totalRessources >= 25000:
                priority = math.inf, UpgradeType.CarryingCapacity
        else:
            if all(i in essentialItems for i in self.playerInfo.carriedItems):
               if level == 4 and totalRessources >= 50000:
                    priority = math.inf, UpgradeType.CarryingCapacity

        return priority
            

    def evaluatePurchase(self):
        return 0

    def go_home(self, gameMap):
        return
        #tiles = normalize_tiles(gameMap, Point(self.ownPos.coords[0], self.ownPos.coords[1]))
        pos = self.PlayerInfo.Position
        pos = Node(pos.x, pos.y)
        house = self.PlayerInfo.HouseLocation
        house = Node(house.x, house.y)
        path = solve_path(tiles, pos, house)
        if path != None:
            point = Point(path[0][0], path[0][1])
            return create_move_action(point)
        else:
            print("something bad happened")
            return create_move_action(Point(-1, 0))

    def before_turn(self, playerInfo):
        """
        Gets called before ExecuteTurn. This is where you get your bot's state.
            :param playerInfo: Your bot's current state.
        """
        self.PlayerInfo = playerInfo

    def execute_turn(self, gameMap, visiblePlayers):
        """
        This is where you decide what action to take.
            :param gameMap: The gamemap.
            :param visiblePlayers:  The list of visible players.
        """
        self.peace -= 1
        if self.prev_score < self.PlayerInfo.Score:
            self.prev_score = self.PlayerInfo.Score
            self.peace = 10

        try:
            pass
            #prev_score = int(StorageHelper.read("points"))
            #if prev_score < self.playerInfo.Score:
            #    StorageHelper.write("peace", 10)
        except:
            pass
            #StorageHelper.write("points", self.PlayerInfo.Score)

        self.ownPos = Node(self.PlayerInfo.Position.x, self.PlayerInfo.Position.y)
        self.housePos = Node(self.PlayerInfo.HouseLocation.x, self.PlayerInfo.HouseLocation.y)
        self.gameMap = gameMap
        self.gameMap._tiles = normalize_tiles(self.gameMap, self.PlayerInfo.Position, self.PlayerInfo.HouseLocation)
        self.visiblePlayers = visiblePlayers

        # GO KILLING LEFT
        if len(self.sortClosest(self.gameMap.tiles, TileContent.Player)) == 1 or self.peace > 0:
            print("test")
            pos = Node(self.PlayerInfo.Position.x, self.PlayerInfo.Position.y)
            print("yMin: ", self.gameMap.yMin)
            yMin = self.gameMap.yMin
            xMin = self.gameMap.xMin
            if yMin < 0:
                yMin = 255 + yMin
            if xMin < 0:
                xMin = 255 + xMin
            Target = Node(xMin, self.PlayerInfo.Position.y)
            self.path = solve_path(self.gameMap._tiles, pos, Target)
            return self.move(self.path)
            #create_move_action(self.path[0])

        Costs = {"ressource": -math.inf, "kill": -math.inf, "upgrade": -math.inf}
        Costs["getRessource"] = self.evaluateRessource()
        Costs["goKill"] = self.evaluatekill()
        Costs["goUpgrade"], item = self.evaluateUpgrade()

        print(Costs)
        nextPlan = max(Costs, key=Costs.get)
        print(nextPlan)

        # PLAN
        nextAction = ""
        if nextPlan == "getRessource":
            self.path = self.ressourcePath
            next_node = Node(self.path[0]+self.ownPos[0], self.path[1]+self.ownPos[1])
            if len(self.path) < 2 and next_node.coords != self.housePos.coords:
                nextAction = "collect"
            else:
                nextAction = "move"

        elif nextPlan == "goKill":
            self.path = self.killingPath
            print(self.path)
            return self.move(self.path)

        elif nextPlan == "goUpgrade":
            self.path = self.upgradePath
            if len(self.path) < 2:
                nextAction = "upgrade"
            else:
                nextAction = "move"
            

        # ACTION
        if nextPlan == "move":
            return create_move_action(self.path[0])
        elif nextAction == "collect":
            return create_collect_action(self.path[0])
        elif nextAction == "attack":
            return create_attack_action(self.path[0])
        elif nextAction == "purchase":
            return create_upgrade_action(item)
        else:
            return create_move_action(Point(-1, 0))

    def after_turn(self):
        """
        Gets called after executeTurn
        """
        pass

    def move(self, path):
        next_node = Point(path[0][0]+self.ownPos.coords[0], path[0][1]+self.ownPos.coords[1])
        if self.gameMap.getTileAt(next_node) == TileContent.Wall or self.gameMap.getTileAt(next_node) == TileContent.Player:
            return create_attack_action(Point(path[0][0], path[0][1]))
        else:
            return create_move_action(Point(path[0][0], path[0][1]))
        