#import optuna
import yaml
#def objective(trial):
#    x = trial.suggest_uniform('x', -10, 10)
#    return (x - 2) ** 2

#study = optuna.create_study()
#study.optimize(objective, n_trials=100)

#study.best_params  # E.g. {'x': 2.002108042}



#def generate_building_cards(num_cards, num_resources, ):
#        card = {}



class BuildingDeck():
    def __init__(self):

        with open("building_cards.yaml") as f:
            card_data = yaml.load(f)

        deck = []
        for card in card_data["deck"]:
            deck += [card["card"]]*card["num"] 

        cards = {x["name"]: x for x in card_data["card"]}
        import pdb; pdb.set_trace()
        
        self.cards = [BuildingsCard(**cards[x]) for x in deck]
    
    def draw_card(self):
        return cards.pop()

class BuildingsCard():
    def __init__(self, name, description, cost, production, victory_points, prerequisite):
        self.name = name # "Wood shop"
        self.cost = cost # e.g {"wood": 5, "money": 10}
        self.production = production # e.g {"wood": 2}
        self.victory_points = victory_points # 2

    def __repr__(self):
        return "<BuildingsCard: {}>".format(self.name)
    
deck = BuildingDeck()
print(deck.cards)