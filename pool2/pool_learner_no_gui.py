import pool2.pool_player
import pool2.pool_simulator
from enum import Enum
import threading


class GameState(Enum):
    Start = 0
    PlayerMove = 1
    Wait = 2
    Simulation = 3
    GameOver = 4


class SimulationResult(Enum):
    Continue = 0
    Switch = 1
    Foul = 2
    P0_Wins = 3
    P1_Wins = 4
    Terminate = 5


def start_in_thread(function_delegate):
    t = threading.Thread(target=function_delegate)
    t.daemon = True
    t.start()


class PoolGameModel(object):

    FULL_COLOR = 0
    STRIPE_COLOR = 1

    def __init__(self, player1, player2, table_width, table_height, ball_size, real_time=False):

        self.stroke_counter = 0

        self.balls_on_table = [] # id, x, y
        self.balls_pocketed = [] # id, player_id
        self.balls_left = [0, 0]
        self.color_assignments = None # 0,1 or 1,0
        # self.foul = False
        self.state = GameState.Start
        self.simulation_result = SimulationResult.Continue
        self.pool_simulator = pool2.pool_simulator.PoolSimulator(table_width, table_height, ball_size)

        self.real_time = real_time

        self.player_id = 0
        self.opponent_id = 1

        self.players = []
        self.players.append(player1)
        self.players.append(player2)

    def switch_players(self):
        tmp_player = self.opponent_id
        self.opponent_id = self.player_id
        self.player_id = tmp_player

    def init_game(self):
        self.stroke_counter = 0
        self.balls_pocketed.clear()
        self.balls_left = [7, 7]
        self.color_assignments = None
        # self.balls_on_table = self.pool_simulator.generate_random_balls()
        self.balls_on_table = self.pool_simulator.pool_rack_em_up()
        self.pool_simulator.set_balls(self.balls_on_table)
        self.players[self.player_id].init(self.player_id,
                                          self.balls_on_table,
                                          self.pool_simulator.get_table_dimensions(),
                                          self.pool_simulator.get_ball_size(),
                                          self.pool_simulator.get_pockets_position())
        self.players[self.opponent_id].init(self.opponent_id,
                                            self.balls_on_table,
                                            self.pool_simulator.get_table_dimensions(),
                                            self.pool_simulator.get_ball_size(),
                                            self.pool_simulator.get_pockets_position())

    def update(self, dt):
        if self.state == GameState.PlayerMove:
            self.state = GameState.Wait
            start_in_thread(self.process_player_move)
        elif self.state == GameState.Wait:
            pass
        elif self.state == GameState.Simulation:
            is_finished = self.pool_simulator.update(dt, step=self.real_time)
            if is_finished:
                self.state = GameState.Wait
                start_in_thread(self.process_simulation_finished)
        elif self.state == GameState.GameOver:
            self.init_game()
            self.state = GameState.PlayerMove
            # print("Game Over: " + str(self.frame_counter))
            pass

    def process_player_move(self):
        print("=====>  Player id: " + str(self.player_id))
        print("Stroke#: " + str(self.stroke_counter))
        print("color assignments: " + str(self.color_assignments))
        print("left [color,stripe] " + str(self.balls_left))
        player = self.players[self.player_id]
        opponent = self.players[self.opponent_id]
        if self.simulation_result == SimulationResult.Foul:
            x, y = player.get_cueball_position()
            self.pool_simulator.reset_cueball(x, y)
            opponent.opponent_cueball_reset(x, y)
        angle, force = player.get_stroke()
        self.pool_simulator.set_stroke(angle, force)
        self.state = GameState.Simulation

    def process_simulation_finished(self):
        self.stroke_counter = self.stroke_counter + 1
        balls_on_table, recently_pocketed_balls, cueball_hits = self.pool_simulator.get_simulation_results()

        # process balls
        self.balls_on_table = balls_on_table

        self.simulation_result = self.check_simulation_state(balls_on_table, recently_pocketed_balls, cueball_hits)

        print("===> simulation result")
        print("color assignments: " + str(self.color_assignments))
        print("left [color,stripe] " + str(self.balls_left))
        print("potted: " + str(recently_pocketed_balls))
        print("cue hits: " + str(cueball_hits))
        # print("foul: " + str(self.foul))
        print("state: " + str(self.simulation_result))
        print("")

        # simulation_result = SimulationState.Continue
        #
        # if len(recently_pocketed_balls) == 0:
        #     simulation_result = SimulationState.Switch
        # else:
        #     for ball in recently_pocketed_balls:
        #         if ball == 0:
        #             self.foul = True
        #             simulation_result = SimulationState.Switch
        #         elif ball == 8:
        #             simulation_result = SimulationState.End_P2Won
        #         else:
        #             # check color assignments
        #             if ball < 8 and self.player_id == 0:
        #                 self.foul = True
        #                 simulation_result = SimulationState.Switch
        #             elif ball > 8 and self.player_id == 1:
        #                 self.foul = True
        #                 simulation_result = SimulationState.Switch
        #         # add to pocketed
        #         self.balls_pocketed.append((ball, self.player_id))

        # todo result should be a class??
        self.players[self.player_id].simulation_results(self.player_id,
                                                        self.stroke_counter,
                                                        self.balls_on_table,
                                                        self.balls_pocketed,
                                                        recently_pocketed_balls,
                                                        cueball_hits,
                                                        self.color_assignments,
                                                        # self.foul,
                                                        self.simulation_result)

        self.players[self.opponent_id].opponent_simulation_results(self.opponent_id,
                                                                   self.stroke_counter,
                                                                   self.balls_on_table,
                                                                   self.balls_pocketed,
                                                                   recently_pocketed_balls,
                                                                   cueball_hits,
                                                                   self.color_assignments,
                                                                   # self.foul,
                                                                   self.simulation_result)
        if self.simulation_result == SimulationResult.Switch or self.simulation_result == SimulationResult.Foul:
            self.switch_players()
            self.state = GameState.PlayerMove
        elif self.simulation_result == SimulationResult.P1_Wins or self.simulation_result == SimulationResult.P0_Wins:
            self.state = GameState.GameOver
        else:
            self.state = GameState.PlayerMove

        if self.stroke_counter % 100 == 0:
            print(self.stroke_counter)
            print(self.state)
            print(self.simulation_result)

    def check_simulation_state(self, balls_on_table, recently_pocketed_balls, cueball_hits):

        simulation_result = SimulationResult.Continue

        if len(cueball_hits) == 0:
            simulation_result = SimulationResult.Foul
        else:
            if self.color_assignments is None:
                if cueball_hits[0] == 8:
                    simulation_result = SimulationResult.Foul
                pass
            else:
                color_assignment = self.color_assignments[self.player_id]
                is_ready_for_the_black = self.balls_left[self.player_id] == 0

                if not is_ready_for_the_black and cueball_hits[0] == 8:
                    simulation_result = SimulationResult.Foul
                elif color_assignment == self.FULL_COLOR:
                    if cueball_hits[0] > 8:
                        simulation_result = SimulationResult.Foul
                        pass
                elif color_assignment == self.STRIPE_COLOR:
                    if cueball_hits[0] < 8:
                        simulation_result = SimulationResult.Foul

        if len(recently_pocketed_balls) > 0:
            for ball in recently_pocketed_balls:
                is_ready_for_the_black = self.balls_left[self.player_id] == 0
                if ball == 0:
                    simulation_result = SimulationResult.Foul
                    pass
                elif ball == 8:
                    winner_helper = {
                        0: SimulationResult.P0_Wins,
                        1: SimulationResult.P1_Wins
                    }
                    if is_ready_for_the_black:
                        return winner_helper[self.player_id]
                    else:
                        return winner_helper[self.opponent_id]
                    pass
                elif ball < 8:
                    self.balls_left[self.FULL_COLOR] -= 1
                    if self.color_assignments is not None and color_assignment != self.FULL_COLOR:
                        simulation_result = SimulationResult.Foul
                elif ball > 8:
                    self.balls_left[self.STRIPE_COLOR] -= 1
                    if self.color_assignments is not None and color_assignment != self.STRIPE_COLOR:
                        simulation_result = SimulationResult.Foul

            # todo: false calor assigment
            if self.color_assignments is None and not simulation_result == SimulationResult.Foul:
                if recently_pocketed_balls[0] < 8:
                    self.color_assignments = [0, 0]
                    self.color_assignments[self.player_id] = self.FULL_COLOR
                    self.color_assignments[self.opponent_id] = self.STRIPE_COLOR
                elif recently_pocketed_balls[0] > 8:
                    self.color_assignments = [0, 0]
                    self.color_assignments[self.player_id] = self.STRIPE_COLOR
                    self.color_assignments[self.opponent_id] = self.FULL_COLOR
                    pass
        elif simulation_result != simulation_result.Foul:
            simulation_result = SimulationResult.Switch

        return simulation_result
