import pyglet
import pymunk.pyglet_util
import pool_world
import time

from pyglet.window import key, mouse


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
        self.cue_angle = 0.0


    def update(self, dt):

        # self.world.update(dt)
        pass

    def on_draw(self):
        self.clear()
        self.fps_display.draw()
        self.world.debug_draw(self.draw_options)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.SPACE:
            f = 120000.0
            # self.world.hit(self.cue_angle, f)
            self.world.hit_and_update_until_finished(self.cue_angle, f)
            self.on_draw()
        elif symbol == key.DOWN:
            self.cue_angle += 0.1
        elif symbol == key.UP:
            self.cue_angle -= 0.2
        elif symbol == key.ESCAPE:
            pyglet.app.exit()
        elif symbol == pyglet.window.key.P:
            pyglet.image.get_buffer_manager().get_color_buffer().save('box2d_vertical_stack.png')

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        print(x)
        print(y)
        pass

if __name__ == '__main__':
    main = Main()
    pyglet.app.run()