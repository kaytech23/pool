"""
Remake of the veritcal stack demo from the box2d testbed.
"""

import math
import time
import pyglet
from pyglet.gl import *
from pyglet.window import key, mouse

from pyglet import gl

import pymunk
from pymunk import Vec2d
import pymunk.pyglet_util


def my_velocity(body, gravity, damping, dt):
    print(body)


def calculate_points(length, x=0, y=0):
    x1 = x
    x2 = x1 + length
    x3 = x2 + length
    y1 = y
    y2 = y1 + length
    return x1, x2, x3, y1, y2


def calculate_gaps(ball_size):
    mid_gap = ball_size * 0.9
    corner_gap = ((mid_gap ** 2) * 2) ** .5
    return corner_gap, mid_gap


class Main(pyglet.window.Window):

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

        pyglet.window.Window.__init__(self, 720, 420, vsync=False)
        # pyglet.window.Window.set_location(self, 20, 200)
        # self.set_caption('Vertical stack from box2d')

        pyglet.clock.schedule_interval(self.update, 1 / 60.0)
        self.fps_display = pyglet.clock.ClockDisplay()
        self.space = pymunk.Space()
        self.space.damping = 0.3
        self.play = True

        pool_lenght = 300
        ball_size = pool_lenght * 2 * 0.024
        print(ball_size)
        self.cue_ball = None
        self.create_table(300, ball_size, 50, 50)
        self.create_balls(ball_size, 300, 50, 50)

        self.draw_options = pymunk.pyglet_util.DrawOptions()
        self.draw_options.flags = self.draw_options.DRAW_SHAPES

        def foul(arbiter, space, data):
            shape = arbiter.shapes[0]
            # space.remove(shape, shape.body)
            shape.body.velocity = (0, 0)
            shape.body.position = (100, 100)
            print("foul")
            return True

        h = self.space.add_collision_handler(self.collision_types["cue"], self.collision_types["pocket"])
        h.begin = foul

        def pocketed(arbiter, space, data):
            shape = arbiter.shapes[0]
            space.remove(shape, shape.body)
            print("ball pocketed: " + str(shape.collision_type))
            return True

        h = self.space.add_collision_handler(self.collision_types["ball"], self.collision_types["pocket"])
        h.begin = pocketed
        self.space.sleep_time_threshold = 0.3
        self.space.idle_speed_threshold = 0.1
        # x1, x2, x3, y1, y2 = calculate_points(300, 50, 50)
        # corner_gap, mid_gap = calculate_gaps(12)

        # print('x1: %d, x2: %d, x3: %d, y1: %d, y2: %d' % (x1, x2, x3, y1, y2))
        # print('c_gap: %s, m_gap: %s' % (corner_gap, mid_gap))
        # self.create_table(300, 12, 50, 50)

    def create_table(self, length, ball_size, x_shift=0, y_shift=0):

        x1, x2, x3, y1, y2 = calculate_points(length, x_shift, y_shift)
        corner_gap, mid_gap = calculate_gaps(ball_size)

        pocket_sensor_dim = 3
        pocket_sensor_dim2 = 8

        lines = [
                # pionowe
                pymunk.Segment(self.space.static_body, (x1, y1 + corner_gap), (x1, y2 - corner_gap), 0),
                # pymunk.Segment(self.space.static_body, (x1 + ball_size, y1 + corner_gap + ball_size), (x1 + ball_size, y2 - corner_gap - ball_size), 0),
                pymunk.Segment(self.space.static_body, (x3, y1 + corner_gap), (x3, y2 - corner_gap), 0),

                # poziome
                pymunk.Segment(self.space.static_body, (x1 + corner_gap, y1), (x2 - mid_gap, y1), 0),
                # pymunk.Segment(self.space.static_body, (x1 + corner_gap + ball_size, y1 + ball_size), (x2 - mid_gap, y1 + ball_size), 0),
                pymunk.Segment(self.space.static_body, (x2 + mid_gap, y1), (x3 - corner_gap, y1), 0),
                pymunk.Segment(self.space.static_body, (x1 + corner_gap, y2), (x2 - mid_gap, y2), 0),
                pymunk.Segment(self.space.static_body, (x2 + mid_gap, y2), (x3 - corner_gap, y2), 0),

                ]
        pockets = [
                pymunk.Circle(self.space.static_body, pocket_sensor_dim2, (x1, y1)),
                pymunk.Circle(self.space.static_body, pocket_sensor_dim2, (x1, y2)),
                pymunk.Circle(self.space.static_body, pocket_sensor_dim, (x2, y1)),
                pymunk.Circle(self.space.static_body, pocket_sensor_dim, (x2, y2)),
                pymunk.Circle(self.space.static_body, pocket_sensor_dim2, (x3, y1)),
                pymunk.Circle(self.space.static_body, pocket_sensor_dim2, (x3, y2))
                ]

        for line in lines:
            line.elasticity = 1.0
            line.friction = 0.0
        for pocket in pockets:
            pocket.elasticity = 1.0
            pocket.friction = 0.0
            pocket.sensor = True
            pocket.collision_type = self.collision_types["pocket"]
        # self.space.sleep_time_threshold = 0.5
        # self.space.idle_speed_threshold = 0.1
        self.space.add(lines)
        self.space.add(pockets)

    def create_balls(self, ball_size, length, x_shift=0, y_shift=0):
        x = 100
        y = 100
        radius = ball_size / 2

        self.cue_ball = self.create_ball(radius, x, y, self.colors["white"], self.collision_types["cue"])
        for i in range(8):
            self.create_ball(radius, 300 + 1 * 50, 105 + i * (ball_size + .1), self.colors["red"],
                             self.collision_types["ball"])
            self.create_ball(radius, 300 + 2 * 50, 105 + i * (ball_size + .1), self.colors["blue"],
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
        self.space.add(body, shape)
        return body


    def update(self, dt):
        # print("update")
        # Here we use a very basic way to keep a set space.step dt.
        # For a real game its probably best to do something more complicated.
        # print("dt: %f" %dt)
        step_dt = 1 / (dt * 40000)
        # print(step_dt)
        x = 0
        while x < dt:
            x += step_dt
            self.space.step(step_dt)

        is_sleeping = True
        for body in self.space.bodies:
            if not body.is_sleeping:
                is_sleeping = False
                break
        if is_sleeping:
            # print("Is sleeping...")
            self.play = True



    def on_draw(self):
        self.clear()
        self.fps_display.draw()
        self.space.debug_draw(self.draw_options)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.SPACE and self.play:
            self.play = False
            f = 180000.0
            self.cue_ball.apply_impulse_at_local_point((f, 0))
        elif symbol == key.DOWN:
            self.cue_ball.angle += 0.1
        elif symbol == key.UP:
            self.cue_ball.angle -= 0.02
        elif symbol == key.ESCAPE:
            pyglet.app.exit()
        elif symbol == pyglet.window.key.P:
            pyglet.image.get_buffer_manager().get_color_buffer().save('box2d_vertical_stack.png')

if __name__ == '__main__':
    main = Main()
    pyglet.app.run()