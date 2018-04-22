import pool_world

class Model(object):

    _game_states = {"waiting": 1, "simulation": 2, "finished": 3}
    _players = {"player 1": 1, "player 2": 2}
    _current_player = _players["player 1"]
    _ball_assignments = {"None": 1, "Colors": 2, "Strips": 3}
    _pocketed_balls = []


    def __init__(self, player1_strategy, player2_strategy):
        self.pool_world = pool_world.World()
        pass

    # getters
    def get_ball_positions(self):
        pass

    def get_table_position(self):
        pass

    def get_game_world(self):
        pass


    # pool table simulator listeners
    def shot_simulation_finished(self, balls_pocketed, cue_hits):
        pass

    def ball_pocketed(self, ball):
        player = self.get_current_player()

    def cue_ball_hit(self, hit):
        pass

    # helpers
    def get_current_player(self):
        pass

# simulator
# current player
# pocketed balls - per player/
# players_colors - None, color, stripe

# game state - waiting, simulation, finished

## external to presenter: get next move from controls
# automatic foul handler : this is player responsibility
# player strategy -> next move: ret force, angle; faul:
# player strategy -> opponent move update

# get balls positions
# get current status
