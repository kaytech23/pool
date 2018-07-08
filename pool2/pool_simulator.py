import pymunk
import random

# https://github.com/viblo/pymunk/blob/master/examples/shapes_for_draw_demos.py


from enum import Enum


def local_color_setter(ball_id):
    if 0 == ball_id:
        return colors["white"]
    elif 8 == ball_id:
        return colors["black"]
    elif 0 < ball_id < 8:
        return colors["blue"]
    else:
        return colors["red"]


colors = {
    "red": (255, 0, 0, 255),
    "white": (255, 255, 255, 255),
    "black": (0, 0, 0, 255),
    "blue": (0, 0, 255, 255)
}

class PoolSimulator(pymunk.Space):

    collision_types = {
        "cueball": 1,
        "notcueball": 2,
        "pocket": 3
    }

    def __init__(self, balls=None, table_length=1200, ball_diameter=24, damping=0.25):
        super(PoolSimulator, self).__init__()

        self.is_finished = True
        self.cue_ball = None
        self.balls_on_table = {}
        self.balls_pocketed = []
        self.balls_hits = []
        self.pockets = []

        self.damping = damping
        self.table_length = table_length
        self.ball_diameter = ball_diameter
        self.sleep_time_threshold = 0.3
        self.idle_speed_threshold = 0.1

        # create world
        self.__create_table(self.table_length, self.ball_diameter)
        self.__setup_collision_handlers()

    def __setup_collision_handlers(self):
        # collisions handlers
        h1 = self.add_collision_handler(self.collision_types["cueball"], self.collision_types["notcueball"])
        h1.begin = self.__cueball_notcueball_collision_handler
        h2 = self.add_collision_handler(self.collision_types["cueball"], self.collision_types["pocket"])
        h2.begin = self.__ball_pocket_collision_handler
        h3 = self.add_collision_handler(self.collision_types["notcueball"], self.collision_types["pocket"])
        h3.begin = self.__ball_pocket_collision_handler

    # collision handlers

    def __cueball_notcueball_collision_handler(self, arbiter, space, data):
        # ball1_id = self.balls_on_table[arbiter.shapes[0]]
        ball_id = self.balls_on_table[arbiter.shapes[1]]
        self.balls_hits.append(ball_id)
        # cueball_id, _ = self.cue_ball
        # if ball1_id == cueball_id:
        #     self.balls_hits.append(ball2_id)
        # elif ball2_id == cueball_id:
        return True

    def __ball_pocket_collision_handler(self, arbiter, space, data):
        shape = arbiter.shapes[0]
        space.remove(shape, shape.body)
        ball_id = self.balls_on_table[shape]
        del self.balls_on_table[shape]
        self.balls_pocketed.append(ball_id)
        return True

    def __create_table(self, inside_table_length, ball_diameter):

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

    def set_balls(self, cueball_id, balls, color_setter=local_color_setter):
        self.__remove_all_balls()
        has_cueball = False
        for ball_id, x, y in balls:
            if cueball_id == ball_id:
                shape = self.__add_ball_to_space(x, y, color_setter(ball_id), self.collision_types["cueball"])
                self.cue_ball = (ball_id, shape)
                has_cueball = True
            else:
                shape = self.__add_ball_to_space(x, y, color_setter(ball_id), self.collision_types["notcueball"])
            self.balls_on_table[shape] = ball_id
        if not has_cueball:
            raise Exception('There is no cue ball')

    # need to test
    def reset_cueball(self, x, y):
        if self.is_finished:
            # clear before
            self.balls_pocketed.clear()
            self.balls_hits.clear()
            cueball_id, shape = self.cue_ball
            self.__remove_ball(shape)
            shape = self.__add_ball_to_space(x, y, colors["white"], self.collision_types["cueball"])
            self.balls_on_table[shape] = cueball_id
            self.cue_ball = (cueball_id, shape)

    def get_cueball_position(self):
        id, shape = self.cue_ball
        return shape.body.position

    def get_balls_position(self):
        balls = []
        for shape in self.balls_on_table.keys():
            ball_id = self.balls_on_table[shape]
            x, y = shape.body.position
            balls.append((ball_id, x, y))
        return balls

    def get_pocketed_balls(self):
        return self.balls_pocketed

    def get_cueball_hits(self):
        return self.balls_hits

    def get_simulation_results(self):
        return self.get_balls_position(), self.pocketed_balls, self.balls_hits

    def simulate_full_stroke(self, angle, force):
        if self.is_finished:
            self.__init_stroke(angle, force)
            while not self.is_finished:
                self.__update(1)
                self.__check_simulation()

    def simulate_interactive_stroke(self, angle, force):
        if self.is_finished:
            self.__init_stroke(angle, force)

    def interactive_update(self, dt):
        self.__update(dt)
        if self.is_finished:
            return True
        else:
            self.__check_simulation()
        return self.is_finished

    def __update(self, dt):
        step_dt = 0.0015
        x = 0
        while x < dt:
            x += step_dt
            self.step(step_dt)

    def __init_stroke(self, angle, force):
        self.is_finished = False
        _, shape = self.cue_ball
        shape.body.angle = angle
        shape.body.apply_impulse_at_local_point((force, 0.0))
        self.balls_pocketed.clear()
        self.balls_hits.clear()

    def __remove_ball(self, shape):
        self.remove(shape)
        del self.balls_on_table[shape]

    def __remove_all_balls(self):
        self.remove(self.balls_on_table.keys())
        self.balls_on_table.clear()

    def __clear_balls_velocity(self):
        for shape in self.balls_on_table.keys():
            shape.body.velocity(0.0, 0.0)

    def __add_ball_to_space(self, x, y, color, collision_type):
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

    def __check_simulation(self):
        for body in self.bodies:
            if not body.is_sleeping:
                self.is_finished = False
                return
        self.is_finished = True

    def generate_random_balls(self):

        random_balls = []

        random_balls.append((0, 100, 100))
        random_balls.append((8, 340, 100))
        shift = self.table_length / 10

        for i in range(1, 8):
            z1 = random.randint(shift, self.table_length - shift)
            z2 = random.randint(shift, self.table_length / 2 - shift)
            random_balls.append((i, z1, z2))

        for i in range(9, 16):
            z1 = random.randint(shift, self.table_length - shift)
            z2 = random.randint(shift, self.table_length / 2 - shift)
            random_balls.append((i, z1, z2))

        return random_balls
