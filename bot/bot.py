from helper import *
import math 


class Bot:
    def __init__(self):
        pass

    def findClosest(self, tiles, type):
        for tile in tiles:
            if tile.TileContent == 4 :
                # ressources[] TODO
        return 0

    def evaluateRessource(self):
        self.gameMap.tiles
        return 0

    def evaluatekill(self):
        return 0

    def evaluateUpgrade(self):

        essentialItems = ["Sword", "Shield", "Backpack"]
        totalRessources = self.PlayerInfo.totalRessources
        level = self.PlayerInfo.getUpgradeLevel(self, self.PlayerInfo.CarryingCapacity)
        priority = -math.inf, None
        
        if level <= 3:
            if level == 1 and totalRessources >= 10000:
                priority = math.inf, UpgradeType.Attack
            if level == 2 and totalRessources >= 15000:
                priority = math.inf, UpgradeType.Attack
            if level == 3 and totalRessources >= 25000:
                priority = math.inf, UpgradeType.Attack
        else:
            if all(i in essentialItems for i in self.playerInfo.carriedItems):
               if level == 4 and totalRessources >= 50000:
                    priority = math.inf, UpgradeType.CarryingCapacity

        return priority
            
    def evaluatePurchase(self):
        
        priority = -math.inf, None
        totalRessources = self.PlayerInfo.totalRessources
        carriedItems = self.playerInfo.carriedItems
        
        if totalRessources >= 30000 and Backpack not in carriedItems:
            priority = math.inf, PurchasableItem.Backpack
        if totalRessources >= 30000 and Backpack in carriedItems and Pickaxe not in carriedItems:
            priority = math.inf, PurchasableItem.Pickaxe
        if totalRessources >= 30000 and Backpack in carriedItems and Pickaxe in carriedItems:
            priority = math.inf, PurchasableItem.Sword

        return priority



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

        # Save house position
        for tile in gameMap.tiles:
            if tile.TileContent == 2:
                housePos = tile.Position

        Costs = {"ressource":0, "kill":0, "upgrade":0}

        Costs["getRessource"] = self.evaluateRessource()
        Costs["goKill"] = self.evaluatekill()
        Costs["goUpgrade"], item = self.evaluateUpgrade()

        nextPlan = max(Costs, key=Costs.get)

        # PLAN
        if nextPlan == "getRessource":
            if len(self.path) < 2 or self.path[0]+self.PlayerInfo.Position == housePos:
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
