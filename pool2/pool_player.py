import pool2

import random


class AIPlayer(object):

    def init(self, table_dimensions, ball_size, pockets_position):
        pass

    def get_stroke(self):
        pass

    def get_stroke_after_foul(self):
        pass

    # frame#, balls_on_table, pocketed_balls, recently_pocketed_balls, cueball_hits, color_assignment, foul, game_over, switch

    # foul: hit wrong color or 8 first, hit no ball at all, pocket cueball, no own color ball pocketed
    # gameover: 8 ball is pocketed, all colors are pocketed


    # def simulation_results(self, balls_on_table, pocketed_balls, recently_pocketed_balls, color_assignment, foul,
    #                        player_switch, is_terminal):
    def simulation_results(self, frame_number, balls_on_table, pocketed_balls, recently_pocketed_balls, cueball_hits, color_assignment, foul, game_over, switch):
        pass

    def opponent_cueball_setup_after_foul(self, x, y):
        pass

    def opponent_simulation_results(self, frame_number, balls_on_table, pocketed_balls, recently_pocketed_balls, cueball_hits, color_assignment, foul, game_over, switch):
        pass


class MyAIPlayer(AIPlayer):

    def init(self, table_dimensions, ball_size, pockets_position):
        pass

    def get_stroke(self):
        angle = random.uniform(0, 3.14)
        force = random.randint(10000, 25000)
        return (angle, force)

    def get_stroke_after_foul(self):
        return (100, 100), self.get_stroke()

    def simulation_results(self, frame_number, balls_on_table, pocketed_balls, recently_pocketed_balls, cueball_hits, color_assignment, foul, game_over, switch):
        return True



class Player(object):

    def init(self):
        pass

    def get_stroke(self):
        return 1.3, 12000

    def get_stroke_after_foul(self):
        return (100, 100), (1.3, 12000)

    def on_key_press(self, symbol):
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        pass


class PlayerWrapper4AIPlayer(object):

    def __init__(self, aiPlayer):
        self.aiPlayer = aiPlayer

    def init(self):
        self.aiPlayer.init()

    def get_stroke(self):
        self.aiPlayer.get_stroke()

    def get_stroke_after_foul(self):
        self.aiPlayer.get_stroke_after_foul()

    def simulation_results(self, balls_on_table, pocketed_balls, recently_pocketed_balls, color_assigment, foul, player_switch, is_terminal):
        self.aiPlayer.simulation_results()

    def opponent_cueball_setup_after_foul(self, x, y):
        pass

    def opponent_simulation_results(self, balls_on_table, pocketed_balls, recently_pocketed_balls, color_assigment, foul, player_switch, is_terminal):
        pass

    def on_key_press(self, symbol):
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        pass