import random

class Player:
    def __init__(self, player_id):
        self.player_id = player_id

        start_items = {
            "Grain": 3,
            "Wood": 3,
        }

        self.market = {} # {item: price}
        self.inventory = start_items # {item: amount}
        self.merchant_pos = "Home"
        self.money = 50
        self.victory_points = 0
        self.buildings = []
    
    def log(self, log_string):
        print("Player {}: {}".format(self.player_id, log_string))
 
    def buy(self, item, amount, other_player):

        cost = other_player.market[item]*amount

        if amount > other_player.inventory[item]:
            self.log("Tried to buy {} items, but only {} available".format(self.money,cost))
            return

        if cost > self.money:
            self.log("Tried to buy {} {} items. Not enough money: {} < {}".format(amount, item,self.money,cost))
            return
            
        # make transaction
        self.money -= cost
        other_player.money += cost
        other_player.inventory[item] -= amount
        self.inventory[item] += amount
        self.log("Buying: {} {}'s for {} from player {}".format(amount, item, cost, other_player.player_id))
        
        
    def set_player_refs(self, other_player):
        # get latest info about other player
        self.other_players = other_player

    def adjust_market(self):
        self.log("adjust market")
        for item, amount in self.inventory.items():
            price = random.randint(10, 50)
            self.market[item] = price
        self.log(self.market)
        self.log(self.inventory)
        
    def trade(self):
        self.log("trade")
        # select fellow merchant
        fellow_merchant = random.choice(self.other_players)
        self.log("Choosing player {} to trade with".format(fellow_merchant.player_id))
        
        item = random.choice(fellow_merchant.market.keys())
        amount = random.randint(0, fellow_merchant.inventory[item])
        self.buy(item, amount, fellow_merchant)
        #import pdb; pdb.set_trace()
        return None

    def build(self):
        print("player {}: build".format(self.player_id))
        return None

    def collect(self):
        print("player {}: collect".format(self.player_id))
        return None
    
