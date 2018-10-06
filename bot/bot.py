from helper import *
import math 

RESSOURCE_BY_BLOC = 1000 # guess
RESSOURCE_BY_PLAYER = 1000 # TODO more details

class Bot:
    def __init__(self):
        pass

    def findClosest(self, tiles, type):
        for tile in tiles:
            if tile.TileContent == type :
                # ressources[] TODO
        return 0

    def evaluateRessource(self):
        closestRessource = self.findClosest(self.gameMap.tiles, 4)
        path = pathFinfing(self.PlayerInfo.position, closestRessource)
        return RESSOURCE_BY_BLOC / len(path)

    def evaluatekill(self):
        closestplayer = self.findClosest(self.gameMap.tiles, 6)
        path = pathFinfing(self.PlayerInfo.position, closestplayer)
        return RESSOURCE_BY_BLOC / len(path)

    def evaluateUpgrade(self):

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
        self.gameMap = gameMap
        self.visiblePlayers = visiblePlayers

        Costs = {"ressource":0, "kill":0, "upgrade":0}

        Costs["getRessource"] = self.evaluateRessource()
        Costs["goKill"] = self.evaluatekill()
        Costs["goUpgrade"], item = self.evaluateUpgrade()

        nextPlan = max(Costs, key=Costs.get)

        # PLAN
        if nextPlan == "getRessource":
            if len(self.path) < 2 or self.path[0]+self.PlayerInfo.Position == self.PlayerInfo.HouseLocation:
                nextAction = "collect"
            else:
                nextAction = "move"

        elif nextPlan == "goKill":
            if len(self.path) < 2:
                nextAction = "attack"
            else:
                nextAction = "move"

        elif nextPlan == "goUpgrade":
            if len(self.path) < 2:
                nextAction = "purchase"
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
            return create_purchase_action(item)


    def after_turn(self):
        """
        Gets called after executeTurn
        """
        pass
