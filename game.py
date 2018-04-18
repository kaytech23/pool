"""
Remake of the veritcal stack demo from the box2d testbed.
"""

import math
import time
import pyglet
from pyglet.gl import *
from pyglet.window import key, mouse

import pymunk
from pymunk import Vec2d
import pymunk.pyglet_util


def my_velocity(body, gravity, damping, dt):
    print(body)

class Main(pyglet.window.Window):
    collision_types = {
        "ball": 1,
        "cue": 2,
        "wall": 3
    }
    cue_ball_body = None

    def __init__(self):

        pyglet.window.Window.__init__(self, 720, 420, vsync=False)
        # pyglet.window.Window.__init__(self)
        self.set_caption('Vertical stack from box2d')

        pyglet.clock.schedule_interval(self.update, 1 / 60.0)
        self.fps_display = pyglet.clock.ClockDisplay()

        self.text = pyglet.text.Label('Press space to fire bullet',
                                      font_size=10,
                                      x=10, y=400)
        self.create_world()

        self.draw_options = pymunk.pyglet_util.DrawOptions()
        self.draw_options.flags = self.draw_options.DRAW_SHAPES

    def create_world(self):
        self.space = pymunk.Space()
        # self.space.gravity = Vec2d(0., 900.)
        self.space.damping = 0.3
        # self.space.bodies.
        # self.space.sleep_time_threshold = 0.3

        # static_body = self.space.static_body
        # static_lines = [pymunk.Segment(static_body, (111.0, 280.0), (407.0, 246.0), 0.0)
        #     , pymunk.Segment(static_body, (407.0, 246.0), (407.0, 343.0), 0.0)
        #                 ]

        x1, y1 = 50, 50
        x2, y2 = 50, 350
        x3, y3 = 650, 50
        x4, y4 = 650, 350

        radius = 12

        static_lines = [pymunk.Segment(self.space.static_body, Vec2d(x1, y1), Vec2d(x2, y2), 0),
                        pymunk.Segment(self.space.static_body, Vec2d(x1, y1), Vec2d(x3, y3), 0),
                        # pymunk.Segment(pymunk.Body(body_type=pymunk.Body.KINEMATIC), Vec2d(550, 55), Vec2d(550, 400), 2),
                        pymunk.Segment(self.space.static_body, Vec2d(x3, y3), Vec2d(x4, y4), 0),
                        pymunk.Segment(self.space.static_body, Vec2d(x2, y2), Vec2d(x4, y4), 0)
                        ]
        for line in static_lines:
            line.elasticity = 1.0
            line.friction = 0.0
            # line.sensor = True
            line.collision_type = self.collision_types["wall"]

        def remove_first(arbiter, space, data):
            ball_shape = arbiter.shapes[0]
            space.remove(ball_shape, ball_shape.body)
            print("ball removed")
            return True

        h = self.space.add_collision_handler(self.collision_types["ball"], self.collision_types["wall"])
        h.begin = remove_first
        self.space.sleep_time_threshold = 0.5
        self.space.idle_speed_threshold = 0.1
        self.space.add(static_lines)

        self.create_cue_ball(50, 160)




        for x in range(4):
            for y in range(x + 1):
                mass = 100.0
                moment = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
                body = pymunk.Body(mass, moment)
                body.position = Vec2d(300 + x * (radius + .1) + y * radius / 2, 105 + y * (radius + .1) + x * radius / 2)

                shape = pymunk.Circle(body, radius, (0, 0))
                # shape.sensor = True
                shape.friction = 0.0
                shape.elasticity = 1.0
                shape.color = (0, 0, 255, 255)
                shape.collision_type = self.collision_types["ball"]
                self.space.add(body, shape)




        # for x in range(2):
        #     for y in range(8):
        #         if x < 1:
        #             color = (0, 0, 255, 255)
        #         else:
        #             color = (124, 3, 0, 125)
        #         size = 12
        #         mass = 100.0
        #         moment = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        #         body = pymunk.Body(mass, moment)
        #         # body.torque = 0.5
        #         body.position = Vec2d(300 + x * 50, 105 + y * (size + .1))
        #
        #         # shape = pymunk.Poly.create_box(body, (size, size))
        #         shape = pymunk.Circle(body, radius, (0, 0))
        #         # shape.sensor = True
        #         shape.friction = 0.0
        #         shape.elasticity = 1.0
        #         shape.color = color
        #         shape.collision_type = self.collision_types["ball"]
        #
        #
        #         # constraint = pymunk.
        #         # constraint.max_bias = 0.0
        #         # constraint.max_force = 1000.0
        #         # body.constraints.add(constraint)
        #         self.space.add(body, shape)
        #         # body.sleep()


    def create_cue_ball(self, x, y):
        mass = 100
        r = 12
        moment = pymunk.moment_for_circle(mass, 0, r, (0, 0))
        body = pymunk.Body(mass, moment)



        body.position = (150, 165)
        shape = pymunk.Circle(body, r, (0, 0))
        shape.friction = 0.0

        shape.elasticity = 1.0
        shape.color = (255, 150, 150, 255)
        shape.collision_type = self.collision_types["cue"]
        # constraint = pymunk.Constraint()
        # constraint.max_bias = 0
        # constraint.max_force = 1000
        # body.constraints.add(constraint)
        self.space.add(body, shape)

        self.cue_ball_body = body

    def update(self, dt):
        # Here we use a very basic way to keep a set space.step dt.
        # For a real game its probably best to do something more complicated.
        # print("dt: %f" %dt)
        step_dt = 1 / (dt * 40000)
        # print(step_dt)
        x = 0
        start = time.time()
        while x < dt:
            x += step_dt
            self.space.step(step_dt)
        # time.sleep(1)
        self.space.sleep_time_threshold = 0.5
        elapsed = time.time() - start

        cnt = 0
        # for body in self.space.bodies:
        #     if body.is_sleeping:
        #        cnt = cnt + 1
        # print('%d is sleeping of %d' % (cnt, len(self.space.bodies)))
            # print(body.velocity)
        # print(self.cue_ball_body.position)
        print(self.cue_ball_body.is_sleeping)
        # print("time: %s, df: %s " % (elapsed, dt))

    def on_key_press(self, symbol, modifiers):
        if symbol == key.SPACE:

            f = 120000.0
            angle = self.cue_ball_body.angle

            f2 = math.sin(angle) * f
            f1 = math.cos(angle) * f
            print("angle: %s", angle)
            print("f1: %d, f2: %d " % (int(f1), int(f2)))
            # impulse = (-53302, 59656) (int(f1), int(f2))
            # impulse = (-53302, 59656)
            # print(impulse)

            self.cue_ball_body.apply_impulse_at_local_point((f, 0))
        elif symbol == key.DOWN:
            self.cue_ball_body.angle += 0.1

        elif symbol == key.ESCAPE:
            pyglet.app.exit()
        elif symbol == pyglet.window.key.P:
            pyglet.image.get_buffer_manager().get_color_buffer().save('box2d_vertical_stack.png')

    def on_draw(self):
        self.clear()
        self.text.draw()
        self.fps_display.draw()
        self.space.debug_draw(self.draw_options)


if __name__ == '__main__':
    main = Main()
    pyglet.app.run()
