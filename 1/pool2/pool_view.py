import pyglet
import pymunk.pyglet_util
import pool2.pool_learner_no_gui

class View(pyglet.window.Window):

    def __init__(self, width, height, model):
        super(View, self).__init__(width, height, vsync=False)

        self.current_player = 1
        self.model = model

        pyglet.gl.glClearColor(0, 0.5, 0, 1)
        self.fps_display = pyglet.clock.ClockDisplay()
        self.draw_options = pymunk.pyglet_util.DrawOptions()
        self.draw_options.flags = self.draw_options.DRAW_SHAPES
        self.label = pyglet.text.Label('Current Player: 1',
                          font_name='Times New Roman',
                          font_size=36,
                          x=20  , y=800,
                          anchor_x='center', anchor_y='center')

    def on_draw(self):
        self.clear()
        self.fps_display.draw()

        self.label = pyglet.text.Label('Current Player: ' + str(self.current_player),
                                       font_name='Times New Roman',
                                       font_size=36,
                                       x=20, y=800,
                                       anchor_x='center', anchor_y='center')
        self.label.draw()
        self.model.debug_draw(self.draw_options)



