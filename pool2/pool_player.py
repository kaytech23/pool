import random
from threading import Semaphore


class Player(object):

    def init(self, player_id, table_dimensions, ball_size, pockets_position):
        self.player_id = player_id
        self.table_dimensions = table_dimensions
        self.pockets_positions = pockets_position

    def get_stroke(self):
        pass

    def get_cueball_position(self):
        pass

    def simulation_results(self, frame_number, balls_on_table, pocketed_balls, recently_pocketed_balls, cueball_hits, color_assignment, is_foul, simulation_state):
        pass

    def opponent_cueball_reset(self, x, y):
        pass

    def opponent_simulation_results(self, frame_number, balls_on_table, pocketed_balls, recently_pocketed_balls, cueball_hits, color_assignment, is_foul, simulation_state):
        pass

    def on_key_press(self, symbol):
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        pass


class AIPlayer(Player):

    def get_stroke(self):
        angle = random.uniform(0, 3.14)
        force = random.randint(10000, 25000)
        return angle, force

    def get_cueball_position(self):
        return 100, 100

    def simulation_results(self, frame_number, balls_on_table, pocketed_balls, recently_pocketed_balls, cueball_hits, color_assignment, is_foul, simulation_state):
        return True

    def opponent_cueball_reset(self, x, y):
        pass

    def opponent_simulation_results(self, frame_number, balls_on_table, pocketed_balls, recently_pocketed_balls, cueball_hits, color_assignment, is_foul, simulation_state):
        pass





class ManualPlayer(Player):

    def __init__(self):
        self.sem1 = Semaphore(1)
        self.sem1.acquire()
        self.sem2 = Semaphore(1)
        self.sem2.acquire()

    def init(self, player_id, table_dimensions, ball_size, pockets_position):
        pass

    def get_stroke(self):
        self.sem1.acquire()
        pass

    def get_cueball_position(self):
        pass

    def on_key_press(self, symbol):
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        pass

#
# class Player(object):
#
#     def init(self):
#         pass
#
#     def get_stroke(self):
#         return 1.3, 12000
#
#     def get_stroke_after_foul(self):
#         return (100, 100), (1.3, 12000)
#
#     def on_key_press(self, symbol):
#         pass
#
#     def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
#         pass
#
#     def on_mouse_press(self, x, y, button, modifiers):
#         pass
#
#
# class ManualPlayer(object):
#     pass
#
#
#
# class AIPlayerWrapper(object):
#
#     def __init__(self, aiPlayer):
#         self.aiPlayer = aiPlayer
#
#     def init(self):
#         self.aiPlayer.init()
#
#     def get_stroke(self):
#         self.aiPlayer.get_stroke()
#
#     def get_stroke_after_foul(self):
#         self.aiPlayer.get_stroke_after_foul()
#
#     def simulation_results(self, balls_on_table, pocketed_balls, recently_pocketed_balls, color_assigment, foul, player_switch, is_terminal):
#         self.aiPlayer.simulation_results()
#
#     def opponent_cueball_setup_after_foul(self, x, y):
#         pass
#
#     def opponent_simulation_results(self, balls_on_table, pocketed_balls, recently_pocketed_balls, color_assigment, foul, player_switch, is_terminal):
#         pass
#
#     def on_key_press(self, symbol):
#         pass
#
#     def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
#         pass
#
#     def on_mouse_press(self, x, y, button, modifiers):
#         pass