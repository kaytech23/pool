import pool2.pool_player
import pool2.pool_simulator

import pyglet
import pymunk.pyglet_util
from pyglet.window import key, mouse

from enum import Enum

import threading

class State(Enum):
    PlayerMove = 1
    Wait = 2
    Simulation = 3
    GameOver = 4


def check_foul(balls_positions, pocketed_balls, cueball_hits, color_assignment, player_id):
    if 0 in pocketed_balls or len(cueball_hits) == 0:
        return True
    if color_assignment != 0:
        if len(cueball_hits) > 0:
            cueball_hits[0] > 8
            return True
    return False


def start_in_thread(function):
    t = threading.Thread(target=function)
    t.daemon = True
    t.start()


def check_color_assignment(pocketed_balls, color_assignment, player_id):
    pass


class AILearner(pyglet.window.Window):

    def __init__(self):
        super(AILearner, self).__init__(1300, 900, vsync=False)

        self.frame_counter = 0

        self.balls_on_table = [] # id, x, y
        self.balls_pocketed = [] # id, player_id
        self.color_assignment = -1 # 0 p1, 1 p2
        self.foul = False
        self.state = State.PlayerMove # start, play, terminal-gameover
        self.pool_simulator = pool2.pool_simulator.PoolSimulator()

        self.player_id = 0
        self.opponent_id = 1

        self.players = []
        self.players.append(pool2.pool_player.MyAIPlayer())
        self.players.append(pool2.pool_player.MyAIPlayer())

        for p in self.players:
            p.init(self.pool_simulator.get_table_dimensions(),
                   self.pool_simulator.get_ball_size(),
                   self.pool_simulator.get_pockets_position())

        self.init_game()
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

    def switch_players(self):
        tmp_player = self.opponent_id
        self.opponent_id = self.player_id
        self.player_id = tmp_player

    def init_game(self):
        self.frame_counter = 0
        self.balls_pocketed.clear()
        self.balls_on_table = self.pool_simulator.generate_random_balls()
        self.pool_simulator.set_balls(0, self.balls_on_table)

    def update(self, dt):
        if self.state == State.PlayerMove:
            self.state = State.Wait
            start_in_thread(self.process_player_move)
        elif self.state == State.Wait:
            pass
        elif self.state == State.Simulation:
            is_finished = self.pool_simulator.step_update(dt)
            if is_finished:
                self.state = State.Wait
                start_in_thread(self.process_simulation_finished)
        elif self.state == State.GameOver:
            print("Game Over")

    def on_draw(self):
        self.clear()
        self.fps_display.draw()

        self.label = pyglet.text.Label('Current Player: ' + str(self.player_id),
                                       font_name='Times New Roman',
                                       font_size=36,
                                       x=20, y=800,
                                       anchor_x='center', anchor_y='center')
        self.label.draw()
        self.pool_simulator.debug_draw(self.draw_options)
        # self.draw_pointer()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.SPACE and self.state == State.GameOver:
            self.init_game()

            self.state = State.PlayerMove

    def process_player_move(self):
        player = self.players[self.player_id]
        opponent = self.players[self.opponent_id]
        if self.foul:
            cueball_position, stroke = player.get_stroke_after_foul()
            x, y = cueball_position
            self.pool_simulator.reset_cueball(x, y)
            opponent.opponent_cueball_setup_after_foul(x, y)
        else:
            stroke = player.get_stroke()
        angle, force = stroke
        self.pool_simulator.set_stroke(angle, force)
        self.state = State.Simulation

    def process_simulation_finished(self):
        self.frame_counter = self.frame_counter + 1

        self.balls_on_table, recently_pocketed_balls, cueball_hits = self.pool_simulator.get_simulation_results()
        for ball in recently_pocketed_balls:
            if ball != 0 and ball != 8:
                self.balls_pocketed.append((ball, self.player_id))

        if len(recently_pocketed_balls) > 0:
            print(self.player_id)
            print(self.balls_on_table)
        # check rules
        # check foul
        # check color assignment
        # player switch ?
        # game state -> play, game_over

        # if self.color_assignment == 0:
        #     self.color_assignment = check_color_assignment(pocketed_balls, self.color_assignment, self.player_id)
        self.foul = check_foul(self.balls_on_table, recently_pocketed_balls, cueball_hits, self.color_assignment, self.player_id)

        # if self.foul:
        #     print('foul')

        switch = True
        game_over = False

        self.players[self.player_id].simulation_results(self.frame_counter,
                                                        self.balls_on_table,
                                                        self.balls_pocketed,
                                                        recently_pocketed_balls,
                                                        cueball_hits,
                                                        self.color_assignment,
                                                        self.foul,
                                                        game_over,
                                                        switch)

        self.players[self.opponent_id].opponent_simulation_results(self.frame_counter,
                                                                   self.balls_on_table,
                                                                   self.balls_pocketed,
                                                                   recently_pocketed_balls,
                                                                   cueball_hits,
                                                                   self.color_assignment,
                                                                   self.foul,
                                                                   game_over,
                                                                   switch)

        self.switch_players()
        if 8 in recently_pocketed_balls:
            self.state = State.GameOver
        else:
            self.state = State.PlayerMove


if __name__ == '__main__':
    main = AILearner()
    pyglet.app.run()

