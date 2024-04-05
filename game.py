from pypokerengine.api.game import setup_config, start_poker
from examples.players.fish_player import FishPlayer
from examples.players.fold_man import FoldMan
from examples.players.honest_player import HonestPlayer
from custompokerplayer import CustomPokerPlayer

config = setup_config(max_round=10, initial_stack=100, small_blind_amount=5)
config.register_player(name="p1", algorithm=FishPlayer())
config.register_player(name="p2", algorithm=FoldMan())
config.register_player(name="p3", algorithm=HonestPlayer())
config.register_player(name="p4", algorithm=CustomPokerPlayer())
game_result = start_poker(config, verbose=1)
