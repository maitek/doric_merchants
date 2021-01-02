import random
from player import Player
from building import BuildingDeck


class Game:
    def __init__(self, num_players):
        # 1. Adjust Market
        # 2. Trade
        # 3. Build
        # 4. Collect
        self.states = ["adjust_market", "trade", "build", "collect"] 
        self.game_state = "Adjust Market" 
        # init players
        self.players = [Player(player_id=x) for x in range(num_players)]
        self.builidng_deck = BuildingDeck()
        self.builidng_deck.shuffle_()
        

        # init players references to other players
        for player in self.players:
            other_players = [x for x in self.players if x != player]
            player.set_player_refs(other_players, self.builidng_deck)
            player.draw_start_cards(self.builidng_deck)
            player.init_inventory({"wood": 5, "grain": 5}, self.builidng_deck)
        
    def run(self):
        
        num_rounds = 10
        self.print_game_stats()

        for round in range(num_rounds):
            print("=== Round {} ===".format(round))
            for state in self.states:
                for player in self.players:
                    # observe game and player states
                    

                    player_state_func = getattr(player, state)
                    player_state_func()
            self.print_game_stats()
        return None

    def print_game_stats(self):
        for player in self.players:
            print("{} {} {} {}".format(player.player_id, player.money, player.inventory, player.victory_points))

if __name__ == "__main__":
    
    for i in range(20):
        
        print("=========== ")
        print("GAME SEED ", i)
        print("=========== ")
        random.seed(i)
        game = Game(num_players=4)
        game.run()




