from enum import Enum


class Player(Enum):
    ONE = 1
    TWO = 2


class GameRules(object):

    # game_state: GameOver, Init, PlayerContinue, PlayerSwitch

    def __init__(self):
        pass

    # game_state, current_player, foul, color_assignment = init_game(player1, player2, table_size)
    def init_game(self):
        pass

    # game_state, current_player, foul, color_assignment = check_turn(balls, balls_pocketed, cue_hit_order)
    def check_game_state(self, balls, balls_pocketed, cue_hit_order):
        pass

    # game_state, current_player, foul, color_assignment = cue_ball_position_reset(x, y)
    def cue_ball_position_reset(self, x, y):
        pass
