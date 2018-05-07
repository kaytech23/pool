

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


from enum import Enum


class BallType(Enum):
    CUE_BALL = 1
    BLACK_BALL = 2
    RED_BALL = 3
    BLUE_BALL = 4


class World(pymunk.Space):

    colors = {
        "red": (255, 0, 0, 255),
        "white": (255, 255, 255, 255),
        "black": (0, 0, 0, 255),
        "blue": (0, 0, 255, 255)
        }

    collision_types = {
        "cue_ball": 1,
        "red_ball": 2,
        "blue_ball": 3,
        "black_ball": 4,
        "cushion": 11,
        "pocket": 10
    }

    def __init__(self, balls=None, table_length=1200, ball_diameter=24, damping=0.25):
        super(World, self).__init__()


        # self.gravity = (-1000, 0)
        # world specification
        self.state = False
        self.damping = damping
        self.table_length = table_length
        self.ball_diameter = ball_diameter
        self.sleep_time_threshold = 0.3
        self.idle_speed_threshold = 0.1

        #Events
        self.game_events = Events()
        self._setup_collision_handlers()

        # world elements data
        self.balls = []
        self.cue_ball = None
        self.black_ball = None
        self.red_balls = []
        self.blue_balls = []
        self.pockets = []

        self.pocketed_balls = []
        self.cue_ball_collisions = []

        # create world
        self._create_table(self.table_length, self.ball_diameter)
        if balls is None:
            balls = self.generate_random_balls()
        self._create_balls(balls)




    def _setup_collision_handlers(self):
        # collisions handlers
        h1 = self.add_collision_handler(self.collision_types["red_ball"], self.collision_types["pocket"])
        h1.begin = self._red_ball_pocketed
        h2 = self.add_collision_handler(self.collision_types["blue_ball"], self.collision_types["pocket"])
        h2.begin = self._blue_ball_pocketed
        h3 = self.add_collision_handler(self.collision_types["cue_ball"], self.collision_types["pocket"])
        h3.begin = self._cueball_pocketed
        h3 = self.add_collision_handler(self.collision_types["black_ball"], self.collision_types["pocket"])
        h3.begin = self._blackball_pocketed
        h4 = self.add_collision_handler(self.collision_types["cue_ball"], self.collision_types["red_ball"])
        h4.begin = self._cueball_hit
        h5 = self.add_collision_handler(self.collision_types["cue_ball"], self.collision_types["blue_ball"])
        h5.begin = self._cueball_hit


    # collision handlers

    # def _color_ball_pocketed(self, arbiter, space, data):


    def _red_ball_pocketed(self, arbiter, space, data):
        shape = arbiter.shapes[0]
        space.remove(shape, shape.body)
        self.balls.remove(shape)
        self.red_balls.remove(shape)
        self.pocketed_balls.append(BallType .RED_BALL)
        self.game_events.on_ball_pocketed(BallType.RED_BALL)
        return True

    def _blue_ball_pocketed(self, arbiter, space, data):
        shape = arbiter.shapes[0]
        space.remove(shape, shape.body)
        self.balls.remove(shape)
        self.blue_balls.remove(shape)
        self.pocketed_balls.append(BallType.BLUE_BALL)
        self.game_events.on_ball_pocketed(BallType.BLUE_BALL)
        return True

    def _cueball_pocketed(self, arbiter, space, data):
        self.pocketed_balls.append(BallType.CUE_BALL)
        self.game_events.on_ball_pocketed(BallType.CUE_BALL)
        return True

    def _blackball_pocketed(self, arbiter, space, data):
        self.pocketed_balls.append(BallType.BLACK_BALL)
        self.game_events.on_ball_pocketed(BallType.BLACK_BALL)
        return True

    def _cueball_hit(self, arbiter, space, data):
        return True

    def _create_table(self, inside_table_length, ball_diameter):

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

        pocket_sensor_diameter = 3 / 4 * self.ball_diameter
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
            self.pockets.append(pocket.body.position)
        self.add(pockets)

        # calc corner gap shift
        # pockets coordinates
        # table corners coordinates
        pass



    def generate_random_balls(self):

        balls = {}
        balls[BallType.CUE_BALL] = (100, 100)
        balls[BallType.BLACK_BALL] = (340, 100)

        red_balls = []
        blue_balls = []

        shift = self.table_length / 10

        for i in range(7):
            z1 = random.randint(shift, self.table_length - shift)
            z2 = random.randint(shift, self.table_length / 2 - shift)
            red_balls.append((z1, z2))
            z1 = random.randint(shift, self.table_length - shift)
            z2 = random.randint(shift, self.table_length / 2 - shift)
            blue_balls.append((z1, z2))

        balls[BallType.RED_BALL] = red_balls
        balls[BallType.BLUE_BALL] = blue_balls

        return balls

    def _create_balls(self, balls):
        for shape in self.balls:
            self.remove(shape.body, shape)
        self.balls.clear()
        self._create_cue_ball(balls[BallType.CUE_BALL])
        self._create_black_ball(balls[BallType.BLACK_BALL])
        self._create_red_balls(balls[BallType.RED_BALL])
        self._create_blue_balls(balls[BallType.BLUE_BALL])

    def _create_cue_ball(self, position):
        self.cue_ball = self._add_ball_to_space(position[0], position[1], self.colors["white"], self.collision_types["cue_ball"])
        self.balls.append(self.cue_ball)

    def _create_black_ball(self, position):
        self.black_ball = self._add_ball_to_space(position[0], position[1], self.colors["black"], self.collision_types["black_ball"])
        self.balls.append(self.black_ball)

    def _create_red_balls(self, positions):
        self.red_balls.clear()
        for position in positions:
            ball = self._add_ball_to_space(position[0], position[1], self.colors["red"], self.collision_types["red_ball"])
            self.red_balls.append(ball)
            self.balls.append(ball)

    def _create_blue_balls(self, positions):
        self.blue_balls.clear()
        for position in positions:
            ball = self._add_ball_to_space(position[0], position[1], self.colors["blue"], self.collision_types["blue_ball"])
            self.blue_balls.append(ball)
            self.balls.append(ball)

    def _add_ball_to_space(self, x, y, color, collision_type):
        mass = 10
        radius = self.ball_diameter / 2
        moment = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, moment)
        body.position = (x, y)
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.friction = 0.0
        shape.elasticity = 1.0
        shape.color = color
        shape.collision_type = collision_type
        self.add(body, shape)
        return shape
    #
    # def add_on_cueball_collision_handler(self, handler):
    #     self.game_events.on_cuehit += handler
    #

    def add_on_simulation_finished_handler(self, handler):
        self.game_events.on_simulation_finished += handler

    def add_on_ball_pocketed_handler(self, handler):
        self.game_events.on_ball_pocketed += handler

    def reset_cueball(self, position):
        if self.state:
            pass
        else:
            self.cue_ball.velocity = (0, 0)
            self.cue_ball.body.position = position

    def reset_balls(self, balls):
        if self.state:
            pass
        else:
            self._create_balls(balls)

    def hit(self, angle, force):
        if self.state:
            pass
        else:
            self.state = True
            self.pocketed_balls = []
            self.cue_ball_collisions = []
            self.cue_ball.body.angle = angle
            self.cue_ball.body.apply_impulse_at_local_point((force, 0.0))

    def update_full(self):
        step_dt = 0.0015
        while self.state:
            self.step(step_dt)
            self.check_state()

    def update(self, dt):
        if self.state:
            step_dt = 1 / (dt * 40000)
            x = 0
            while x < dt:
                x += step_dt
                self.step(step_dt)
            self.check_state()

    def check_state(self):
        is_sleeping = True
        for body in self.bodies:
            if not body.is_sleeping:
                is_sleeping = False
                break
        if is_sleeping:
            balls = self.get_balls_positions()
            self.state = False
            self.game_events.on_simulation_finished(balls, self.pocketed_balls, None)
            return True
        return False

    def get_balls_positions(self):
        balls = {
            BallType.CUE_BALL: self.get_cue_ball_position(),
            BallType.BLACK_BALL: self.get_black_ball_position(),
            BallType.RED_BALL: self.get_red_balls_positions(),
            BallType.BLUE_BALL: self.get_blue_balls_positions()
        }
        return balls

    # get pocket positions
    # get last_stroke pocketed_balls
    # get last_stroke cue_balls_hits

    def get_cue_ball_position(self):
        return self.cue_ball.body.position

    def get_black_ball_position(self):
        return self.black_ball.body.position

    def get_red_balls_positions(self):
        balls = []
        for ball in self.red_balls:
            balls.append(ball.body.position)
        return balls

    def get_blue_balls_positions(self):
        balls = []
        for ball in self.blue_balls:
            balls.append(ball.body.position)
        return balls

