

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
import random
from events import Events

# https://github.com/viblo/pymunk/blob/master/examples/shapes_for_draw_demos.py


# def calculate_points(length, x=0, y=0):
#     x1 = x
#     x2 = x1 + length
#     x3 = x2 + length
#     y1 = y
#     y2 = y1 + length
#     return x1, x2, x3, y1, y2
#
#
# def calculate_gaps(ball_size):
#     mid_gap = ball_size
#     corner_gap = ((mid_gap ** 2) * 2) ** .5
#     return corner_gap, mid_gap

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
        super(World, self).__init__()
        self.game_events = Events()
        self.damping = 0.35
        self.state = False

        # h = self.add_collision_handler(1, 2)
        # h.begin = self.pocketed
        # self.create_table(300, 12)

        self.cue_ball = None
        self.reset_table_data(600, 12)
        self.create_balls(12)



        h1 = self.add_collision_handler(self.collision_types["ball"], self.collision_types["pocket"])
        h1.begin = self.pocketed
        h2 = self.add_collision_handler(self.collision_types["cue"], self.collision_types["pocket"])
        h2.begin = self.pocketed


        self.sleep_time_threshold = 0.3
        self.idle_speed_threshold = 0.1

    def pocketed(self, arbiter, space, data):
        shape = arbiter.shapes[0]
        space.remove(shape, shape.body)
        # print("ball pocketed: ")
        print("ball pocketed: " + str(shape.collision_type))
        return True

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

        import operator


        pocket_sensor_diameter = 9
        pockets_coordinates = {}
        pockets_coordinates["Top_Left"] = tuple(map(operator.add, table_corners["Top_Left"], (corner_shift / 2, -corner_shift /2)))
        pockets_coordinates["Top_Right"] = tuple(map(operator.add, table_corners["Top_Right"], (-corner_shift / 2, -corner_shift /2)))
        pockets_coordinates["Down_Left"] = tuple(map(operator.add, table_corners["Down_Left"], (corner_shift / 2, corner_shift /2)))
        pockets_coordinates["Down_Right"] = tuple(map(operator.add, table_corners["Down_Right"], (-corner_shift / 2, corner_shift / 2)))
        table_half_length = table_length / 2
        pockets_coordinates["Top_Mid"] = (table_half_length, table_width)
        pockets_coordinates["Down_Mid"] = (table_half_length, 0)
        pockets = [
                pymunk.Circle(self.static_body, pocket_sensor_diameter, pockets_coordinates["Top_Left"]),
                pymunk.Circle(self.static_body, pocket_sensor_diameter, pockets_coordinates["Top_Right"]),
                pymunk.Circle(self.static_body, pocket_sensor_diameter, pockets_coordinates["Down_Left"]),
                pymunk.Circle(self.static_body, pocket_sensor_diameter, pockets_coordinates["Down_Right"]),
                pymunk.Circle(self.static_body, pocket_sensor_diameter, pockets_coordinates["Top_Mid"]),
                pymunk.Circle(self.static_body, pocket_sensor_diameter, pockets_coordinates["Down_Mid"])
                ]

        for pocket in pockets:
            pocket.elasticity = 1.0
            pocket.friction = 0.0
            pocket.sensor = True
            pocket.collision_type = self.collision_types["pocket"]
        self.add(pockets)

        # calc corner gap shift
        # pockets coordinates
        # table corners coordinates
        pass

    def create_balls(self, ball_size):
        x = 100
        y = 100
        radius = ball_size / 2

        self.cue_ball = self.create_ball(radius, x, y, self.colors["white"], self.collision_types["cue"])

        for i in range(8):
            z1 = random.randint(1, 5)
            z2 = random.randint(1, 3)
            self.create_ball(radius, 300 + z1 * 50, 105 + z2 * (ball_size + .1), self.colors["red"],
                             self.collision_types["ball"])
            self.create_ball(radius, 300 + z2 * 50, 105 + z2 * (ball_size + .1), self.colors["blue"],
                             self.collision_types["ball"])


        # black_ball = self.create_ball(radius, x, y)

    def create_ball(self, radius, x, y, color, collision_type):
        mass = 100
        moment = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, moment)
        body.position = (x, y)
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.friction = 0.0
        shape.elasticity = 1.0
        shape.color = color
        shape.collision_type = collision_type
        self.add(body, shape)
        return body

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
        if self.state:
            pass
        else:
            self.state = True
            self.cue_ball.angle = angle
            self.cue_ball.apply_impulse_at_local_point((force, 0.0))


    def update(self, dt):
        step_dt = 1 / (dt * 40000)
        x = 0
        while x < dt:
            x += step_dt
            self.step(step_dt)
        # self.check_state()

    def check_state(self):
        is_sleeping = True
        for body in self.bodies:
            if not body.is_sleeping:
                is_sleeping = False
                break
        if is_sleeping:
            # print("Is sleeping...")
            self.state = False
            return True
        return False

    def update_until_finish(self):
        step_dt = 0.0015
        self.step(step_dt)

        while self.check_state():
            self.step(step_dt)
        pass

    def hit_and_update_until_finished(self, angle, force):
        self.hit(angle, force)
        self.update_until_finish()
        pass


    # simulation
    # def pocketed(self, arbiter, space, data):
    #     self.ball_pocketed()
    #     return True

