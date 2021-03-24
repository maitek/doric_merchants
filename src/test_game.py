from game import Game


def test_player_init_inventory():
    init_inventory = {"wood": 5, "grain": 10}
    game = Game(4,init_inventory)
    for player in game.players:
        for item in player.inventory:
            if item in init_inventory.values():
                assert player.inventory[item] == init_inventory[item]
            else:
                assert player.inventory[item] == 0
            


#def test_player_buy():
#    game = Game(num_players=4,init_inventory={"wood": 15, "grain": 15})
#    game.players[0].inventory
#    import pdb; pdb.set_trace()

#player_buy()
test_player_init_inventory()