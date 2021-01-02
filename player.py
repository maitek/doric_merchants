import random

class Player:
    def __init__(self, player_id):
        self.player_id = player_id

        start_items = {
            "grain": 5,
            "wood": 5,
        }

        self.market = {} # {item: price}
        self.inventory = start_items # {item: amount}
        self.merchant_pos = "Home"
        self.money = 50
        self.victory_points = 0
        self.buildings = []
        self.building_card_hand = []
    
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

    def init_inventory(self,start_inventory,building_deck):
        # init inventory
        all_resources = building_deck.get_all_resources()
        self.inventory = dict()
        for item in all_resources:
            self.inventory[item] = 0
        for key, value in start_inventory.items():
            self.inventory[key] = value


    def draw_start_cards(self, building_deck):
        for i in range(5):
            card = building_deck.draw_card()
            self.building_card_hand.append(card)

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
        can_build_buildings = [(i,x) for i, x in enumerate(self.building_card_hand) if x.can_build(self.inventory)]
        if len(can_build_buildings) > 0:
            to_build_choice = random.choice(can_build_buildings)
            to_build_idx = to_build_choice[0]
            to_build = to_build_choice[1]
            for item, cost in to_build.cost.items():
                self.inventory[item] -= cost
                self.buildings.append(to_build)
                self.building_card_hand.pop(to_build_idx)

        # change building card action
        if len(self.building_card_hand) > 0: 
            to_change_idx = random.randint(0,len(self.building_card_hand)-1)
            self.building_card_hand.pop(to_change_idx)

        # TODO discard pile

        # draw cards to fill hand
        while self.building_card_hand < 5:
            card = building_deck.draw_card()
            self.building_card_hand.append(card)

        return None

    def collect(self):
        print("player {}: collect".format(self.player_id))

        # collect resources
        for building in self.buildings:
            for production_option in building.production:
                
                # TODO choose what to produce

                # pay production cost
                for item_name, item_amount in production_option["cost"].items():
                    self.inventory[item_name] -= item_amount
                
                # get produced items
                for item_name, item_amount in production_option["result"].items():
                    self.inventory[item_name] += item_amount
        return None
    

