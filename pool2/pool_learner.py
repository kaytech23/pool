import pool2.pool_player
from enum import Enum

class Players(Enum):
    Player = 1
    Opponent = 2

class AILearner(object):

    def __init__(self):
        self.players.append(pool2.pool_player.Player())
        self.players.append(pool2.pool_player.Player())

        self.balls_on_table = [] # id, x, y
        self.balls_pocketed = [] # id, player_id
        self.balls_recently_pocketed_in_order = [] # ids, player_id
        self.color_assignment = 0 # 0 - None, 1, 2 player - with full colors
        self.foul = False
        self.state = 0 # start, play, terminal-gameover

    def switch_players(self):
        tmp_player = self.players[Players.Player]
        self.players[Players.Player] = self.players[Players.Opponent]
        self.players[Players.Opponent] = tmp_player


    def main_loop(self):
        init_game()
        state = game_play
        while game_play
            if foul:
                cue_ball_position = current_player.get_foul_cueball_position()
                pool_simulator.update_cueball(cue_ball_position)
                if no foul -> inform opponent about cueball
            angle, force = current_player.get_player_move()
            pool_simulator.set_stroke_full(angle, force)
            check_foul
            switch/continue check_move
            pool_siulatore.getresult()
            inform player and opponent about results(balls positions, balls_pocketed, recently_pocketed, foul, color_assignment, is_terminal_state, continue)

