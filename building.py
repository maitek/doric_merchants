#import optuna
import yaml
import random
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
        
        self.cards = [BuildingsCard(**cards[x]) for x in deck]
    
    def draw_card(self):
        return self.cards.pop()
    
    def shuffle_(self):
        random.shuffle(self.cards)

class BuildingsCard():
    def __init__(self, name, description, cost, production, victory_points):
        self.name = name
        self.description = description
        self.cost = {x.split(" ")[1]: float(x.split(" ")[0]) for x in cost}
        self.production = production 
        self.victory_points = victory_points

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
    
