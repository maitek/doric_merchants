#import optuna
import yaml
import random
from copy import deepcopy
#def objective(trial):
#    x = trial.suggest_uniform('x', -10, 10)
#    return (x - 2) ** 2

#study = optuna.create_study()
#study.optimize(objective, n_trials=100)

#study.best_params  # E.g. {'x': 2.002108042}

class BuildingDeck():
    def __init__(self):

        with open("building_cards.yaml") as f:
            card_data = yaml.safe_load(f)

        deck = []
        for card in card_data["deck"]:
            deck += [card["card"]]*card["num"] 

        cards = {x["name"]: x for x in card_data["card"]}
        self.cards = [BuildingsCard(**deepcopy(cards[x])) for x in deck]

        resource_list = set()
        for card in self.cards:
            #import pdb; pdb.set_trace()
            for production_option in card.production:
                for item in production_option["result"]:
                    resource_list.add(item)
        self.all_resource_list = list(resource_list)

    def draw_card(self):
        return self.cards.pop()

    def discard_card(self,card):
        return self.cards.append(card)
    
    def shuffle_(self):
        random.shuffle(self.cards)

class BuildingsCard():
    def __init__(self, name, description, cost, production, victory_points):
        self.name = name
        self.description = description
        self.cost = self.parse_item_cost(cost)
        #print(self.name, production)
        self.production = production
        for idx, production_option in enumerate(self.production):
            self.production[idx]["cost"] = self.parse_item_cost(production_option.get("cost", []))
            self.production[idx]["result"] = self.parse_item_cost(production_option.get("result",[])) 
           
        self.victory_points = victory_points

        

    def parse_item_cost(self, item_list):
        #print("item",item_list)
        # convert ["2 grain", "4 stone"] into {"grain": 2, "stone": 4}
        return {x.split(" ")[1]: float(x.split(" ")[0]) for x in item_list}


    def can_build(self, inventory):
        # Return true if inventory is available to build building
        for item, cost in self.cost.items():
            if item not in inventory.keys():
                # item not available
                return False 
            else:
                if cost > inventory[item]:
                    # item available but not enough
                    return False 
        # item available and enough to build   
        return True
    
        
    def __repr__(self):
        return "<BuildingsCard: {}>".format(self.name)


from collections import Counter

if __name__ == "__main__":
    deck = BuildingDeck()
    print(deck.all_resource_list)

    card_dict = dict()
    card_counter = Counter([x.name for x in deck.cards])


    #relative_value_items = avg_production/game / total_production/game
    #max_production/game = num_producer_cards*num_items_per_producer
    #max_

    # theorietical max items that can be produces in one round
    max_production_dict = dict()
    for resource in deck.all_resource_list:
            max_production_per_round = 0
            for key in card_counter.keys():
                card_instance = next(x for x in deck.cards if x.name == key)
                for production_option in card_instance.production:
                    #import pdb; pdb.set_trace()
                    max_items_per_producer = production_option["result"].get(resource, 0)
                    max_production_per_round += card_counter[key] * max_items_per_producer
                    max_production_dict[resource] = max_production_per_round
    
    print("max_production_per_round",max_production_dict)

     # theorietical max items that can be consumed in one round
    max_consumption_dict = dict()
    for resource in deck.all_resource_list:
            max_consumpion_per_round = 0
            for key in card_counter.keys():
                card_instance = next(x for x in deck.cards if x.name == key)
                # building cost
                building_cost = card_instance.cost.get(resource, 0)
                max_consumpion_per_round += card_counter[key] * building_cost
                for production_option in card_instance.production:
                    # production cost
                    max_items_per_producer = production_option["cost"].get(resource, 0)
                    max_consumpion_per_round += card_counter[key] * max_items_per_producer
                    
                    max_consumption_dict[resource] = max_consumpion_per_round
    
    print("max_consumpion_per_round",max_consumption_dict)

    for key in max_consumption_dict.keys():
        value = max_consumption_dict[key]/max_production_dict[key]
        print(key, value)




# ==============================
# Unit tests
def test_building_can_buld():
    card = BuildingsCard(name="", description="", cost=["5 wood", "3 grain"], production={}, victory_points=0)
    inventory = {"wood": 5, "grain": 3}
    assert card.can_build(inventory) == True
    inventory = {"wood": 5, "grain": 2}
    assert card.can_build(inventory) == False

def test_deck_draw_card():
    deck = BuildingDeck()
    num_cards = len(deck.cards)
    card = deck.draw_card()
    assert len(deck.cards) == num_cards-1
    
