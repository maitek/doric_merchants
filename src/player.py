import random
from copy import copy

class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.market = {} # {item: price}
        self.inventory = {} # {item: amount}
        self.merchant_pos = "Home"
        self.money = 50
        self.victory_points = 0
        self.buildings = []
        self.building_card_hand = []

        # bookeeping history
        self.player_inventory_history = list()
        self.player_money_history = list()
  
    def log(self, log_string):
        print("Player {}: {}".format(self.player_id, log_string))
 
    def buy(self, item, amount, other_player):
        
        cost = other_player.market[item]*amount
       
        if amount > other_player.inventory[item]:
            raise Exception("Tried to buy {} {} items, but only {} available".format(amount,item,other_player.inventory[item]))
            
        if self.money < cost:
            raise Exception("Tried to buy {} {} items. Not enough money: {} < {}".format(amount, item,self.money,cost))
            
        # make transaction
        self.money -= cost
        other_player.money += cost
        other_player.inventory[item] -= amount
        self.inventory[item] += amount
        self.log("Buying: {} {}'s for {} from player {}, {}$ left".format(amount, item, cost, other_player.player_id, self.money))
        
        
    def set_player_refs(self, other_players_ref, building_deck_ref):
        # get latest info about other player
        self.other_players_ref = other_players_ref
        self.building_deck_ref = building_deck_ref

    def init_inventory(self,start_inventory,building_deck):
        # init inventory
        all_resources = building_deck.all_resource_list
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
        self.log("ADJUST MARKET")
        # Player adjusts market price of its inventory items
        self.market = {}
        for item, amount in self.inventory.items():
            if amount > 0:
                price = random.randint(5, 20)
                self.market[item] = price
        self.log({x:"{} / {}$".format(self.inventory[x],y) for x,y in self.market.items()})

        


    def trade(self):
        self.log("TRADE")
        # Player select a fellow merchant player to trade with
        fellow_merchant = random.choice(self.other_players_ref)
        self.log("Choosing player {} to trade with".format(fellow_merchant.player_id))

        can_afford_items = [x for x,y in fellow_merchant.market.items() if y <= self.money]
        if len(can_afford_items) > 0:
            item = random.choice(can_afford_items)
            price = fellow_merchant.market[item]
            max_amount = self.money // price
            max_amount = min(max_amount,fellow_merchant.inventory[item])
            if max_amount > 1:
                amount = random.randint(1, max_amount)
                self.buy(item, amount, fellow_merchant)            
            
        return None

    def build(self):
        self.log("BUILD")
        # build building action
        
        can_build_buildings = [(i,x) for i, x in enumerate(self.building_card_hand) if x.can_build(self.inventory)]
        if len(can_build_buildings) > 0:
            to_build_choice = random.choice(can_build_buildings)
            to_build_idx = to_build_choice[0]
            to_build = to_build_choice[1]
            
            # pay building cost
            for item, cost in to_build.cost.items():
                self.inventory[item] -= cost
            self.log("building {} at cost {} ".format(to_build.name,to_build.cost))
            # build
            self.buildings.append(to_build)
            self.building_card_hand.pop(to_build_idx)
        else:
            self.log("Cant build any of {}".format([x.name for x in self.building_card_hand]))
        # change building card action
        if len(self.building_card_hand) > 0: 
            to_change_idx = random.randint(0,len(self.building_card_hand)-1)
            discard_card = self.building_card_hand[to_change_idx]
            self.building_card_hand.pop(to_change_idx)
            self.building_deck_ref.discard_card(discard_card)

        # TODO discard pile

        # draw cards to fill hand
        while len(self.building_card_hand) < 5:
            card = self.building_deck_ref.draw_card()
            self.building_card_hand.append(card)

        return None

    def collect(self):
        self.log("COLLECT")

        # collect resources
        for building in self.buildings:

            # choose among production options
            can_afford_options = []
            for production_option in building.production:
                can_afford = True
                for item_name, item_amount in production_option["cost"].items():
                    if self.inventory[item_name] - item_amount < 0: 
                        can_afford = False
                if can_afford:
                    can_afford_options.append(production_option)

            if len(can_afford_options) > 0:
                # select what to produce
                production_option = random.choice(can_afford_options)

                # pay production cost
                for item_name, item_amount in production_option["cost"].items():
                    self.inventory[item_name] -= item_amount

                # get produced items
                for item_name, item_amount in production_option["result"].items():
                    self.inventory[item_name] += item_amount
                self.log("Producing {} {} from {} at cost {}".format(item_amount,item_name,building.name,production_option["cost"]))
                
        return None

    def log_data(self):
            self.player_inventory_history.append(copy(self.inventory))
            self.player_money_history.append(copy(self.money))
    


# ==============================
# Unit tests

def test_player_buy():
    players = [Player(player_id=x) for x in range(2)]
    builidng_deck = BuildingDeck()
    

# Bug, inventory goes to negative