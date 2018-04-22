

# setup environment

# stroke -> angle, force
# strokeAndSimulate -> angle,force : ret ball positions
# update(number of steps) -> returns ball positions
# updateUntilFinished() -> returns ball positions
# get(ball positions)
# reset(ball positions)
# simulation_state = finished, in-progress
# events: ball pocketed, simulation finished, cue_ball_hit
import pymunk
from events import Events


def calculate_points(length, x=0, y=0):
    x1 = x
    x2 = x1 + length
    x3 = x2 + length
    y1 = y
    y2 = y1 + length
    return x1, x2, x3, y1, y2


def calculate_gaps(ball_size):
    mid_gap = ball_size
    corner_gap = ((mid_gap ** 2) * 2) ** .5
    return corner_gap, mid_gap

class World(pymunk.Space):

    def __init__(self):
        self.game_events = Events()
        pymunk.Space.__init__(self)
        self.damping = 0.3
        h = self.add_collision_handler(1, 2)
        h.begin = self.pocketed
        self.create_table(300, 12)
        self.create_balls()

    def create_table(self, length, ball_size, x_shift=0, y_shift=0):

        x1, x2, x3, y1, y2 = calculate_points(length, x_shift, y_shift)
        corner_gap, mid_gap = calculate_gaps(ball_size)

        pocket_sensor_dim = 3
        pocket_sensor_dim2 = 8

        xa = x1
        xb = x1 + 12

        ya = y1 + corner_gap
        yb = y2 - corner_gap

        lines = [
            # pionowe
            # pymunk.Segment(self.static_body, (x1, y1 + corner_gap), (x1, y2 - corner_gap), 0),
            pymunk.Poly(self.static_body, [(xa, ya), (xb, yb), (xa, yb), (xb, ya)]),
            # pymunk.Segment(self.space.static_body, (x1 + ball_size, y1 + corner_gap + ball_size), (x1 + ball_size, y2 - corner_gap - ball_size), 0),
            # pymunk.Segment(self.space.static_body, (x1, y1 + corner_gap),
            #                (x1 + ball_size, y1 + corner_gap + ball_size), 0),
            pymunk.Segment(self.static_body, (x3, y1 + corner_gap), (x3, y2 - corner_gap), 0),

            # poziome
            pymunk.Segment(self.static_body, (x1 + corner_gap, y1), (x2 - mid_gap, y1), 0),
            # pymunk.Segment(self.space.static_body, (x1 + corner_gap + ball_size, y1 + ball_size), (x2 - mid_gap, y1 + ball_size), 0),
            pymunk.Segment(self.static_body, (x2 + mid_gap, y1), (x3 - corner_gap, y1), 0),
            pymunk.Segment(self.static_body, (x1 + corner_gap, y2), (x2 - mid_gap, y2), 0),
            pymunk.Segment(self.static_body, (x2 + mid_gap, y2), (x3 - corner_gap, y2), 0),

        ]
        for line in lines:
            line.elasticity = 1.0
            line.friction = 0.0
        self.add(lines)

    def add_on_cuehit_handler(self, handler):
        self.game_events.on_cuehit += handler

    def add_on_gamestate_changed_handler(self, handler):
        self.game_events.on_gamestate_changed += handler

    def add_on_ball_pocketed_handler(self, handler):
        self.game_events.on_ball_pocketed += handler

    # init


    def create_balls(self):
        pass

    def create_ball(self):
        # black
        # cue
        # stripes
        # full
        pass

    # strokes
    def hit(self, angle, force):
        pass

    def update(self, steps):
        pass

    def update_until_finish(self):
        pass

    def hit_and_update_until_finished(self, angle, force):
        self.hit(angle, force)
        self.update_until_finish()
        pass


    # simulation
    def pocketed(self, arbiter, space, data):
        self.ball_pocketed()
        return True

