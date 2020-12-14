import random

class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        #self.hand = Hand()
        #self.town = Town()

        start_items = {
            "Wood": random.randint(0,5),
            "Stone": random.randint(0,5),
            "Gold": random.randint(0,5),
        }

        self.market_prices = {} # {item: price}
        self.inventory = start_items # {item: amount}
        self.merchant_pos = "Home"
        self.money = 10
        self.victory_points = 0
        
        # store state the player knows about the game
        self.observations = {}

    def sharable_info(self):
        # info to be shared with other players
        shareble_info = {
            "player_id": self.player_id,
            "market_price": self.market_prices
        }
        return shareble_info

    def observe(self, other_player_info):
        # get latest info about other player
        self.observations["other_player_info"] = other_player_info

    def adjust_market(self):
        print("player {}: adjust market".format(self.player_id))
        for item, amount in self.inventory.items():
            price = random.randint(10, 20)
            self.market_prices[item] = price
        print(self.market_prices)
        print(self.inventory)
        
    def trade(self):
        print("player {}: trade".format(self.player_id))
        # select fellow merchant
        options = [x["player_id"] for x in self.observations["other_player_info"]]
        options = [x for x in options if x != self.player_id]
        fellow_merchant = random.choice(options)
        print("Player {} choose player {} to trade with".format(self.player_id,fellow_merchant))

        
        return None

    def build(self):
        print("player {}: build".format(self.player_id))
        return None

    def collect(self):
        print("player {}: collect".format(self.player_id))
        return None
    
