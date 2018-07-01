import pyglet
import pymunk.pyglet_util
import pool_world
import random
import math
import time

from pyglet.window import key, mouse

# games state: onprogress -> finished
# current player
# player_one_state: pockted balls, color



class Main(pyglet.window.Window):

    def __init__(self):
        super(Main, self).__init__(1300, 900, vsync=False)
        pyglet.gl.glClearColor(0, 0.5, 0, 1)

        self.current_player = 1

        pyglet.clock.schedule_interval(self.update, 1 / 60.0)
        self.fps_display = pyglet.clock.ClockDisplay()
        self.world = pool_world.World()
        self.world.add_on_ball_pocketed_handler(self.ball_pocketed)
        self.world.add_on_simulation_finished_handler(self.on_simulation_finished)

        self.draw_options = pymunk.pyglet_util.DrawOptions()
        self.draw_options.flags = self.draw_options.DRAW_SHAPES
        self.cue_angle = 0.0
        self.pointer_line = (0, 0, 0, 0)

        self.real_time = False

        self.label = pyglet.text.Label('Current Player: 1',
                          font_name='Times New Roman',
                          font_size=36,
                          x=20  , y=800,
                          anchor_x='center', anchor_y='center')

    def calculate_point_on_circle(self, cx, cy, r, angle):
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        return x, y

    def ball_pocketed(self, pocketed_ball):
        print("Ball pockted handler: " + str(pocketed_ball))

    def change_current_player(self):
        if self.current_player == 1:
            self.current_player = 2
        else:
            self.current_player = 1
        self.label.text = 'Current Player: ' + str(self.current_player)

    def update(self, dt):

        if self.real_time:
            self.world.update(dt)
        else:
            self.world.update_full()

    def calculate_line(self):
        cue_position = self.world.get_cue_ball_position()
        x, y = self.calculate_point_on_circle(cue_position[0], cue_position[1], 1040, self.cue_angle)
        self.pointer_line = (int(cue_position[0]), int(cue_position[1]), int(x), int(y))

    def draw_pointer(self):
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', self.pointer_line))
        # pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (0, 0, 10, 10)))

    def on_draw(self):
        self.clear()
        self.fps_display.draw()
        self.label.draw()
        self.world.debug_draw(self.draw_options)
        self.draw_pointer()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.SPACE:
            f = 25000.0
            self.world.hit(self.cue_angle, f)
        elif symbol == key.DOWN:
            self.cue_angle += 0.03
            self.calculate_line()
        elif symbol == key.UP:
            self.cue_angle -= 0.1
            self.calculate_line()
        elif symbol == key.ESCAPE:
            pyglet.app.exit()
        elif symbol == pyglet.window.key.P:
            pyglet.image.get_buffer_manager().get_color_buffer().save('box2d_vertical_stack.png')

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        print(x)
        print(y)
        # self.real_time = not self.real_time
        self.world.reset_cueball( (x, y))
        self.calculate_line()
        pass

    # ball_states = []

    def on_simulation_finished(self, balls, pocketed_balls, cueball_hits):
        # self.ball_states.append(balls)
        print("Red + Bules: " + str(len(balls[pool_world.BallType.BLUE_BALL]) + len(balls[pool_world.BallType.RED_BALL])))
        self.calculate_line()

        print("Cue ball position: " + str(balls[pool_world.BallType.CUE_BALL]))
        print("Number of pocketed balls: " + str(len(pocketed_balls)))
        for ball in pocketed_balls:
            print("Pocketd: " + str(ball))

        # if len(pocketed_balls) == 0:
        #     self.change_current_player()

        angle, force = self.calculate_next_shot(balls)

        for ball in pocketed_balls:
            if ball == pool_world.BallType.CUE_BALL:
                self.world.reset_cueball((100, 100))

        # print(angle)
        # print(force)
        # self.on_draw()
        # self.update(1)
        # self.world.hit(angle, force)

        # idx = random.randint(0, len(self.ball_states) - 1)
        # print("setting world to state: " + str(idx) + " of " + str(len(self.ball_states)))
        # self.world.reset_balls(self.ball_states[idx])

    def calculate_next_shot(self, balls):
        angle = random.random() * 6
        force = 24000.0
        return angle, force


if __name__ == '__main__':
    main = Main()
    pyglet.app.run()