import pyglet
import pymunk.pyglet_util
import pool_world
import time


class Main(pyglet.window.Window):

    def __init__(self):
        pyglet.window.Window.__init__(self, 720, 420, vsync=False)
        # pyglet.window.Window.set_location(self, 20, 200)
        # self.set_caption('Vertical stack from box2d')

        pyglet.clock.schedule_interval(self.update, 1 / 60.0)
        self.fps_display = pyglet.clock.ClockDisplay()
        self.world = pool_world.World()
        self.draw_options = pymunk.pyglet_util.DrawOptions()
        self.draw_options.flags = self.draw_options.DRAW_SHAPES
        self.hit = False

        self.start_time = time.time()

    def update(self, dt):
        step_dt = 1 / (dt * 40000)
        # print(step_dt)
        x = 0
        while x < dt:
            x += step_dt
            self.world.update(step_dt)

        elapsed = time.time() - self.start_time
        if 2 < elapsed and not self.hit:
            self.world.hit(1, 1)
            self.hit = True

    def on_draw(self):
        self.clear()
        self.fps_display.draw()
        self.world.debug_draw(self.draw_options)


if __name__ == '__main__':
    main = Main()
    pyglet.app.run()