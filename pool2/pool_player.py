import random
import math


class Player(object):

    def __init__(self):
        self.player_id = -1
        self.table_dimensions = None
        self.ball_size = None
        self.pocket_positions = None
        self.color_assignments = None
        self.balls_on_table = []

    def init(self, player_id, balls_on_table, table_dimensions, ball_size, pockets_position):
        self.player_id = player_id
        self.balls_on_table = balls_on_table
        self.table_dimensions = table_dimensions
        self.ball_size = ball_size
        self.pocket_positions = pockets_position

    def get_stroke(self):
        pass

    def get_cueball_position(self):
        pass

    def simulation_results(self, player_id, stroke_number, balls_on_table, pocketed_balls, recently_pocketed_balls, cueball_hits, color_assignments, simulation_state):
        pass

    def opponent_cueball_reset(self, x, y):
        pass

    def opponent_simulation_results(self, player_id, stroke_number, balls_on_table, pocketed_balls, recently_pocketed_balls, cueball_hits, color_assignments, simulation_state):
        pass

    def on_key_press(self, symbol):
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        pass


class AbstractAIPlayer(Player):

    def __init__(self):
        super(Player).__init__()
        self.last_player_id = -1
        self.stroke_number = 0
        self.pocketed_balls = []
        self.recently_pocketed_balls = []
        self.cueball_hits = []
        self.is_foul = False
        self.simulation_state = None

    def init(self, player_id, balls_on_table, table_dimensions, ball_size, pockets_position):
        Player.init(self, player_id, balls_on_table, table_dimensions, ball_size, pockets_position)
        self.stroke_number = 0
        self.pocketed_balls = []
        self.recently_pocketed_balls = []
        self.cueball_hits = []
        self.is_foul = False
        self.simulation_state = None

    def get_stroke(self):
        pass

    def get_cueball_position(self):
        pass

    def simulation_results(self, player_id, stroke_number, balls_on_table, pocketed_balls, recently_pocketed_balls, cueball_hits, color_assignments, simulation_state):
        self.last_player_id = player_id
        self.stroke_number = stroke_number
        self.pocketed_balls = pocketed_balls
        self.recently_pocketed_balls = recently_pocketed_balls
        self.balls_on_table = balls_on_table
        self.pocketed_balls = pocketed_balls
        self.cueball_hits = cueball_hits
        self.color_assignments = color_assignments
        self.simulation_state = simulation_state
        self.on_simulation_finish()

    def opponent_cueball_reset(self, x, y):
        for ball in self.balls_on_table:
            if ball[0] == 0:
                self.balls_on_table.remove(ball)
                break
        self.balls_on_table.append((0, float(x), float(y)))
        self.on_opponent_cueball_reset()

    def opponent_simulation_results(self, player_id, stroke_number, balls_on_table, pocketed_balls, recently_pocketed_balls, cueball_hits, color_assignments, simulation_state):
        self.last_player_id = player_id
        self.stroke_number = stroke_number
        self.pocketed_balls = pocketed_balls
        self.recently_pocketed_balls = recently_pocketed_balls
        self.balls_on_table = balls_on_table
        self.pocketed_balls = pocketed_balls
        self.cueball_hits = cueball_hits
        self.color_assignments = color_assignments
        self.simulation_state = simulation_state
        self.on_opponent_simulation_finish()

    def get_my_color_assignment(self):
        if self.color_assignments is None:
            return None
        return self.color_assignments[self.player_id]

    def on_simulation_finish(self):
        pass

    def on_opponent_simulation_finish(self):
        pass

    def on_opponent_cueball_reset(self):
        pass


class AIPlayer(AbstractAIPlayer):

    def get_stroke(self):
        angle = random.uniform(0, 3.14)
        force = random.randint(10000, 25000)
        return angle, force

    def get_cueball_position(self):
        return 100, 100

    def on_simulation_finish(self):
        pass

    def on_opponent_simulation_finish(self):
        pass

    def on_opponent_cueball_reset(self):
        pass


class AISimulatorPlayer(AbstractAIPlayer):

    def get_stroke(self):

        black_ball = None
        cue_ball = None
        # if self.color_assignments is None:
        for id, x, y in self.balls_on_table:
            if id == 8:
                black_ball = (id, x, y)
                continue
            elif id == 0:
                cue_ball = (id, x, y)

        for key, pocket in self.pocket_positions.items():
            # pocket = self.pocket_positions["Top_Right"]
            # pocket = (pocket[0] - 15, pocket[1] - 15)
            angle1 = math.atan2(pocket[1] - black_ball[2], pocket[0] - black_ball[1])
            if 0 < angle1 < 1.57:
                print(key)
                print(angle1)
                break

        if black_ball[1] < cue_ball[1]:
            x = black_ball[1] + math.cos(angle1) * self.ball_size
        else:
            x = black_ball[1] - math.cos(angle1) * self.ball_size

        if black_ball[2] < cue_ball[2]:
            y = black_ball[2] + math.sin(angle1) * self.ball_size
        else:
            y = black_ball[2] - math.sin(angle1) * self.ball_size

        # y = math.sin(angle1) * self.ball_size

        ghost_ball = (x, y)

        print(pocket)
        print(black_ball)
        print(ghost_ball)

        angle = math.atan2(cue_ball[2] - ghost_ball[1], cue_ball[1] - ghost_ball[0]) + 3.14
        force = random.randint(10000, 18000)
        return angle, force

    def get_cueball_position(self):
        return random.randint(100, 200), random.randint(100, 200)

    def on_simulation_finish(self):
        pass

    def on_opponent_simulation_finish(self):
        pass

    def on_opponent_cueball_reset(self):
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