from helper import *


class Bot:
    def __init__(self):
        pass

    def evaluateRessource(self):
        return 0

    def evaluatekill(self):
        return 0

    def evaluateUpgrade(self):
        self.path
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

        Costs = {"ressource":0, "kill":0, "upgrade":0}

        Costs["getRessource"] = self.evaluateRessource()
        Costs["goKill"] = self.evaluatekill()
        Costs["goUpgrade"], item = self.evaluateUpgrade()

        nextPlan = max(Costs, key=Costs.get)

        # PLAN
        if nextPlan == "getRessource":
            if len(self.path) < 2:
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
