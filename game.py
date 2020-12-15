from player import Player

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

        # init players references to other players
        for player in self.players:
            other_players = [x for x in self.players if x != player]
            player.set_player_refs(other_players)

    def run(self):
        
        num_rounds = 2
        
        for round in range(num_rounds):
            print("=== Round {} ===".format(round))
            for state in self.states:
                for player in self.players:
                    # observe game and player states
                    

                    player_state_func = getattr(player, state)
                    player_state_func()
        return None

if __name__ == "__main__":
    game = Game(num_players=4)
    game.run()




