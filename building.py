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
            card_data = yaml.load(f)

        deck = []
        for card in card_data["deck"]:
            deck += [card["card"]]*card["num"] 

        cards = {x["name"]: x for x in card_data["card"]}
        
        self.cards = [BuildingsCard(**cards[x]) for x in deck]
    
    def draw_card(self):
        return cards.pop()
    
    def shuffle(self):
        random.shuffle(self.cards)

class BuildingsCard():
    def __init__(self, name, description, cost, production, victory_points):
        self.name = name
        self.description = description
        self.cost = {x.split(" ")[1]: float(x.split(" ")[0]) for x in cost}
        self.production = production 
        self.victory_points = victory_points

    def __repr__(self):
        return "<BuildingsCard: {}>".format(self.name)

    
deck = BuildingDeck()
print(deck.cards)
deck.shuffle()
#import pdb; pdb.set_trace()
print(deck.cards)