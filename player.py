import random

class Player:
    def __init__(self, player_id):
        self.player_id = player_id

        start_items = {
            "Grain": 10,
            "Wood": 10,
        }

        self.market = {} # {item: price}
        self.inventory = start_items # {item: amount}
        self.merchant_pos = "Home"
        self.money = 50
        self.victory_points = 0
        self.buildings = []
        self.building_cards = []
    
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
        
        
    def set_player_refs(self, other_players_ref, building_deck_ref):
        # get latest info about other player
        self.other_players_ref = other_players_ref
        self.building_deck_ref = building_deck_ref

    def draw_start_cards(self, building_deck):
        for i in range(5):
            card = building_deck.draw_card()
            self.building_cards.append(card)

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
        fellow_merchant = random.choice(self.other_players_ref)
        self.log("Choosing player {} to trade with".format(fellow_merchant.player_id))
        
        item = random.choice(fellow_merchant.market.keys())
        amount = random.randint(0, fellow_merchant.inventory[item])
        self.buy(item, amount, fellow_merchant)
        #import pdb; pdb.set_trace()
        return None

    def build(self):
        print("player {}: build".format(self.player_id))
        # build building action
        can_build_buildings = [x for x in self.building_cards if x.can_build(self.inventory)]
        
        if len(can_build_buildings) > 0:
            to_build = random.choice(can_build_buildings)
            import pdb; pdb.set_trace()
        # TODO discard card action
        return None

    def collect(self):
        print("player {}: collect".format(self.player_id))
        # collect resources
        for building in self.buildings:
            for item in building.production:
                produced_items = item["results"]
            import pdb; pdb.set_trace()
            self.inventory[item] += amount

        # update victory points

        # update money
        return None
    

