import pool2.pool_player
import pool2.pool_simulator
import pool2.pool_game_state

import pyglet
import pymunk.pyglet_util
from pyglet.window import key, mouse

from enum import Enum

import threading


class GameState(Enum):
    Start = 0
    PlayerMove = 1
    Wait = 2
    Simulation = 3
    GameOver = 4


class SimulationState(Enum):
    Continue = 0
    Switch = 1
    P1Won = 2
    P2Won = 3
    Terminated = 4


def start_in_thread(function_delegate):
    t = threading.Thread(target=function_delegate)
    t.daemon = True
    t.start()

class AILearner(pyglet.window.Window):

    def __init__(self):
        super(AILearner, self).__init__(1300, 900, vsync=False)

        self.frame_counter = 0

        self.balls_on_table = [] # id, x, y
        self.balls_pocketed = [] # id, player_id
        self.color_assignment = -1 # 0 p1, 1 p2
        self.foul = False
        self.state = GameState.Start
        self.simulation_state = SimulationState.Continue
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
        if self.state == GameState.PlayerMove:
            self.state = GameState.Wait
            start_in_thread(self.process_player_move)
        elif self.state == GameState.Wait:
            pass
        elif self.state == GameState.Simulation:
            is_finished = self.pool_simulator.full_update()
            if is_finished:
                self.state = GameState.Wait
                start_in_thread(self.process_simulation_finished)
        elif self.state == GameState.GameOver:
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
        if symbol == key.SPACE and (self.state == GameState.GameOver or self.state == GameState.Start):
            self.init_game()
            self.state = GameState.PlayerMove

    def process_player_move(self):
        player = self.players[self.player_id]
        opponent = self.players[self.opponent_id]
        if self.foul:
            x, y = player.get_cueball_position()
            self.pool_simulator.reset_cueball(x, y)
            opponent.opponent_cueball_reset(x, y)
        angle, force = player.get_stroke()
        self.pool_simulator.set_stroke(angle, force)
        self.state = GameState.Simulation

    def process_simulation_finished(self):
        self.frame_counter = self.frame_counter + 1
        balls_on_table, recently_pocketed_balls, cueball_hits = self.pool_simulator.get_simulation_results()

        # process balls
        self.balls_on_table = balls_on_table

        if len(recently_pocketed_balls) == 0:
            self.simulation_state = SimulationState.Switch
        else:
            for ball in recently_pocketed_balls:
                if ball == 0:
                    self.foul = True
                    self.simulation_state = SimulationState.Switch
                elif ball == 8:
                    self.simulation_state = SimulationState.P2Won
                else:
                    # check color assignments
                    if ball < 8 and self.player_id == 0:
                        self.foul = True
                        self.simulation_state = SimulationState.Switch
                    elif ball > 8 and self.player_id == 1:
                        self.foul = True
                        self.simulation_state = SimulationState.Switch
                # add to pocketed
                self.balls_pocketed.append((ball, self.player_id))

        # game_state = SimulationState.Continue # continue, switch, p1_won, p2_won, terminated
        # self.check_game_rules(balls_on_table, recently_pocketed_balls, cueball_hits)

        self.players[self.player_id].simulation_results(self.frame_counter,
                                                        self.balls_on_table,
                                                        self.balls_pocketed,
                                                        recently_pocketed_balls,
                                                        cueball_hits,
                                                        self.color_assignment,
                                                        self.foul,
                                                        self.simulation_state)

        self.players[self.opponent_id].opponent_simulation_results(self.frame_counter,
                                                                   self.balls_on_table,
                                                                   self.balls_pocketed,
                                                                   recently_pocketed_balls,
                                                                   cueball_hits,
                                                                   self.color_assignment,
                                                                   self.foul,
                                                                   self.simulation_state)
        if self.simulation_state == SimulationState.Switch:
            self.switch_players()
            self.state = GameState.PlayerMove
        elif self.simulation_state == SimulationState.P2Won or self.simulation_state == SimulationState.P1Won:
            self.state = GameState.GameOver
        else:
            self.state = GameState.PlayerMove

        print(self.frame_counter)
        print(self.state)
        print(self.simulation_state)
        print(self.foul)


if __name__ == '__main__':
    main = AILearner()
    pyglet.app.run()

