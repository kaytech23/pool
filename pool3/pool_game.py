import pyglet
import pymunk.pyglet_util
import pool_learner_no_gui
import pool_player

from pyglet.window import key, mouse

# https://www.quora.com/How-do-you-calculate-what-angle-to-hit-a-pool-ball

class Game(pyglet.window.Window):

    TABLE_WIDTH = 1200
    TABLE_HEIGHT = 600
    BALL_SIZE = 24

    def __init__(self):
        super(Game, self).__init__(1300, 900, vsync=False)

        # player1 = pool_player.AIPlayer()
        player1 = pool_player.AISimulatorPlayer()
        player2 = pool_player.AISimulatorPlayer()

        self.model = pool_learner_no_gui.PoolGameModel(player1, player2, self.TABLE_WIDTH, self.TABLE_HEIGHT, self.BALL_SIZE, real_time=True)

        pyglet.gl.glClearColor(0, 0.5, 0, 1)
        pyglet.clock.schedule_interval(self.update, 1 / 60.0)
        self.fps_display = pyglet.clock.ClockDisplay()
        self.draw_options = pymunk.pyglet_util.DrawOptions()
        self.draw_options.flags = self.draw_options.DRAW_SHAPES
        self.label = pyglet.text.Label('Current Player: 1',
                          font_name='Times New Roman',
                          font_size=36,
                          x=20  , y=800,
                          anchor_x='center', anchor_y='center')

    def update(self, dt):
        self.model.update(dt)

    def on_draw(self):
        self.clear()
        self.fps_display.draw()

        self.label = pyglet.text.Label('Current Player: ' + str(self.model.player_id),
                                       font_name='Times New Roman',
                                       font_size=36,
                                       x=20, y=800,
                                       anchor_x='center', anchor_y='center')
        self.label.draw()
        self.model.pool_simulator.debug_draw(self.draw_options)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.SPACE and (self.model.state == pool_learner_no_gui.GameState.GameOver
                                    or self.model.state == pool_learner_no_gui.GameState.Start):
            self.model.init_game()
            self.model.state = pool_learner_no_gui.GameState.PlayerMove


if __name__ == '__main__':
    main = Game()
    pyglet.app.run()
