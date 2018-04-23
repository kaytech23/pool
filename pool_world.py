

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

# https://github.com/viblo/pymunk/blob/master/examples/shapes_for_draw_demos.py


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

    colors = {
        "red": (124, 3, 0, 125),
        "white": (255, 255, 255, 255),
        "black": (1, 4, 6, 7),
        "blue": (0, 0, 255, 255),
        "green": (54, 54, 54, 54)
        }

    collision_types = {
        "ball": 1,
        "cue": 2,
        "wall": 3,
        "pocket": 4
    }


    def __init__(self):
        self.game_events = Events()
        pymunk.Space.__init__(self)
        self.damping = 0.35

        # h = self.add_collision_handler(1, 2)
        # h.begin = self.pocketed
        # self.create_table(300, 12)

        self.reset_table_data(550, 12)
        self.create_balls(12)



    def reset_table_data(self, inside_table_length, ball_diameter):

        # shifts
        ball_radius = ball_diameter / 2
        center_shift = ball_diameter * 2
        corner_shift = center_shift / (2 ** 0.5)

        inside_table_width = inside_table_length / 2
        table_length = inside_table_length + 2 * corner_shift
        table_width = inside_table_width + 2 * corner_shift

        table_corners = {"Down_Left": (0.0, 0.0), "Top_Left": (0.0, table_width),
                         "Top_Right": (table_length, table_width), "Down_Right": (table_length, 0.0)}

        cussions = {}
        cussions["Left"] = [
            (0, corner_shift),
            (0, table_width - corner_shift),
            (ball_diameter, corner_shift + ball_diameter),
            (ball_diameter, table_width - corner_shift - ball_diameter)
        ]
        cussions["Right"] = [
            (table_length, corner_shift),
            (table_length, table_width - corner_shift),
            (table_length - ball_diameter, corner_shift + ball_diameter),
            (table_length - ball_diameter, table_width - corner_shift - ball_diameter)
        ]
        cussions["Down_Left"] = [
            (corner_shift, 0),
            (table_length / 2 - center_shift / 2, 0),
            (corner_shift + ball_diameter, ball_diameter),
            (table_length / 2 - center_shift / 2 - ball_diameter / 2, ball_diameter)
        ]
        cussions["Down_Right"] = [
            (table_length / 2 + center_shift / 2, 0),
            (table_length - corner_shift, 0),
            (table_length / 2 + center_shift / 2 + ball_diameter / 2, ball_diameter),
            (table_length - corner_shift - ball_diameter, ball_diameter)
        ]
        cussions["Up_Left"] = [
            (corner_shift, table_width),
            (table_length / 2 - center_shift / 2, table_width),
            (corner_shift + ball_diameter, table_width - ball_diameter),
            (table_length / 2 - center_shift / 2 - ball_diameter / 2, table_width - ball_diameter)
        ]

        cussions["Up_Right"] = [
            (table_length / 2 + center_shift / 2, table_width),
            (table_length - corner_shift, table_width),
            (table_length / 2 + center_shift / 2 + ball_diameter / 2, table_width - ball_diameter),
            (table_length - corner_shift - ball_diameter, table_width - ball_diameter)
        ]

        # mass = 100
        # moment = pymunk.moment_for_poly(mass, cussions["Right"])
        # body = pymunk.Body(mass, moment, body_type=pymunk.Body.STATIC)


        lines = [
            pymunk.Poly(self.static_body, cussions["Left"]),
            pymunk.Poly(self.static_body, cussions["Right"]),
            pymunk.Poly(self.static_body, cussions["Up_Right"]),
            pymunk.Poly(self.static_body, cussions["Up_Left"]),
            pymunk.Poly(self.static_body, cussions["Down_Right"]),
            pymunk.Poly(self.static_body, cussions["Down_Left"])
        ]

        for line in lines:
            line.elasticity = 1.0
            line.friction = 0.0
            # self.add(body, line)
        self.add(lines)


        # calc corner gap shift
        # pockets coordinates
        # table corners coordinates
        pass

    def create_balls(self, ball_size):
        x = 500
        y = 100
        radius = ball_size / 2

        self.cue_ball = self.create_ball(radius, x, y, self.colors["white"], self.collision_types["cue"])

        # for i in range(8):
        #     z1 = random.randint(1, 5)
        #     z2 = random.randint(1, 3)
        #     self.create_ball(radius, 300 + z1 * 50, 105 + z2 * (ball_size + .1), self.colors["red"],
        #                      self.collision_types["ball"])
        #     self.create_ball(radius, 300 + z2 * 50, 105 + z2 * (ball_size + .1), self.colors["blue"],
        #                      self.collision_types["ball"])


        # black_ball = self.create_ball(radius, x, y)

    def create_ball(self, radius, x, y, color, collision_type):
        mass = 100
        moment = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, moment)
        body.position = (x, y)
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.friction = 1.0
        shape.elasticity = 1.0
        shape.color = color
        # shape.collision_type = collision_type
        self.add(body, shape)
        return body


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
            pymunk.Poly(self.static_body, [(xa, ya), (xb, yb - 12), (xa, yb), (xb, ya + 12)]),
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

    #
    # def create_balls(self):
    #     pass

    # def create_ball(self):
    #     # black
    #     # cue
    #     # stripes
    #     # full
    #     pass

    # strokes
    def hit(self, angle, force):
        f = 180000.0
        self.cue_ball.apply_impulse_at_local_point((f/3, f/4))
        pass

    def update(self, steps):
        self.step(steps)
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

