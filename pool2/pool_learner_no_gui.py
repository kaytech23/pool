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


class SimulationState(Enum):
    Continue = 0
    Switch = 1
    End_P1Won = 2
    End_P2Won = 3
    Terminate = 4


def start_in_thread(function_delegate):
    t = threading.Thread(target=function_delegate)
    t.daemon = True
    t.start()


class PoolGameModel(object):

    def __init__(self, player1, player2, realtime=False):

        self.frame_counter = 0

        self.balls_on_table = [] # id, x, y
        self.balls_pocketed = [] # id, player_id
        self.color_assignment = None # 0 p1, 1 p2
        self.foul = False
        self.state = GameState.Start
        self.pool_simulator = pool2.pool_simulator.PoolSimulator()

        self.player_id = 0
        self.opponent_id = 1

        self.players = []
        self.players.append(player1)
        self.players.append(player2)

        player1.init(self.player_id,
                     self.pool_simulator.get_table_dimensions(),
                     self.pool_simulator.get_ball_size(),
                     self.pool_simulator.get_pockets_position())

        player2.init(self.opponent_id,
                     self.pool_simulator.get_table_dimensions(),
                     self.pool_simulator.get_ball_size(),
                     self.pool_simulator.get_pockets_position())

    def switch_players(self):
        tmp_player = self.opponent_id
        self.opponent_id = self.player_id
        self.player_id = tmp_player

    def init_game(self):
        self.frame_counter = 0
        self.balls_pocketed.clear()
        # self.balls_on_table = self.pool_simulator.generate_random_balls()
        self.balls_on_table = self.pool_simulator.pool_rack_em_up()
        self.pool_simulator.set_balls(self.balls_on_table)

    def update(self, dt):
        if self.state == GameState.PlayerMove:
            self.state = GameState.Wait
            start_in_thread(self.process_player_move)
        elif self.state == GameState.Wait:
            pass
        elif self.state == GameState.Simulation:
            is_finished = self.pool_simulator.step_update(dt)
            if is_finished:
                self.state = GameState.Wait
                start_in_thread(self.process_simulation_finished)
        elif self.state == GameState.GameOver:
            print("Game Over: " + str(self.frame_counter))

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

        simulation_state = SimulationState.Continue

        if len(recently_pocketed_balls) == 0:
            simulation_state = SimulationState.Switch
        else:
            for ball in recently_pocketed_balls:
                if ball == 0:
                    self.foul = True
                    simulation_state = SimulationState.Switch
                elif ball == 8:
                    simulation_state = SimulationState.End_P2Won
                else:
                    # check color assignments
                    if ball < 8 and self.player_id == 0:
                        self.foul = True
                        simulation_state = SimulationState.Switch
                    elif ball > 8 and self.player_id == 1:
                        self.foul = True
                        simulation_state = SimulationState.Switch
                # add to pocketed
                self.balls_pocketed.append((ball, self.player_id))

        self.players[self.player_id].simulation_results(self.frame_counter,
                                                        self.balls_on_table,
                                                        self.balls_pocketed,
                                                        recently_pocketed_balls,
                                                        cueball_hits,
                                                        self.color_assignment,
                                                        self.foul,
                                                        simulation_state)

        self.players[self.opponent_id].opponent_simulation_results(self.frame_counter,
                                                                   self.balls_on_table,
                                                                   self.balls_pocketed,
                                                                   recently_pocketed_balls,
                                                                   cueball_hits,
                                                                   self.color_assignment,
                                                                   self.foul,
                                                                   simulation_state)
        if simulation_state == SimulationState.Switch:
            self.switch_players()
            self.state = GameState.PlayerMove
        elif simulation_state == SimulationState.End_P2Won or simulation_state == SimulationState.End_P1Won:
            self.state = GameState.GameOver
        else:
            self.state = GameState.PlayerMove

        if self.frame_counter % 100 == 0:
            print(self.frame_counter)
            print(self.state)
            print(simulation_state)
            print(self.foul)


    def check_simulation_state(self, balls_on_table, recently_pocketed_balls, cueball_hits):

        self.balls_on_table = balls_on_table

        is_ready_for_the_black = is_ready_for_the_black()
        color_assingment = get_player_color_assigment()

        # check first ball contact
            # none
            # black
            # correct/incorect color
        # check potted balls
            # cue faule
            # black end of the game
                # if ready for black
                # not ready
            # check assigment and rest colors



    # def check_rules(self, ReadyForTheBlack, ColorAssignment, FirstBallBallContact,
    #                Player, PotCount, BallPotSeq, UnpottedBalls,
    #                BallLocationX, BallLocationY, BallDiameter, WhiteLineX, TableWidth):
        PoolMsg = '';
        Foul = 0;
        EndofGame = 0;

        if ReadyForTheBlack[Player - 1] == 0:
            CannotStrikeBlack = 1;
        else:
            CannotStrikeBlack = 0;

        if FirstBallBallContact == 0:
            PoolMsg = 'FOUL! Player {0} Failed to Hit a Ball'.format(Player)
            Foul = 1;
        else:
            if ColorAssignment[Player - 1] == 1:
                if FirstBallBallContact > 8 - CannotStrikeBlack:
                    PoolMsg = 'FOUL! Player {0} First Hit Ball of Wrong Color'.format(Player)
                    Foul = 1;
            elif ColorAssignment[Player - 1] == 2:
                if FirstBallBallContact < 8 + CannotStrikeBlack:
                    PoolMsg = 'FOUL! Player {0} First Hit Ball of Wrong Color'.format(Player)
                    Foul = 1;

        if PotCount > 0:
            for J in range(0, PotCount):
                if BallPotSeq[J] == 0:
                    PoolMsg = 'FOUL! Player {0} Potted the Cue Ball'.format(Player)
                    BallLocationX[0] = WhiteLineX;
                    BallLocationY[0] = TableWidth / 2;
                    UnpottedBalls.append(0)
                    UnpottedBalls.sort()
                    Foul = 1;
                    for K in range(J + 1, PotCount):
                        BallLocationX[BallPotSeq[K]] = BallLocationX[BallPotSeq[K]] - (BallDiameter + 0.01);
                elif BallPotSeq[J] == 8:
                    EndofGame = 1;
                    if ReadyForTheBlack[Player - 1] == 0:
                        PoolMsg = 'FOUL! Player {0} Potted the Black Ball'.format(Player)
                        Foul = 1;
                else:
                    PoolMsg = 'Player {0} Potted the {1}, ball'.format(Player, BallPotSeq[J])
                    if max(ColorAssignment) == 0:
                        if Player == 1:
                            if BallPotSeq[J] < 8:
                                ColorAssignment = [1, 2]
                                PoolMsg = 'Player 1 is Yellow, Player 2 is Blue'
                            elif BallPotSeq[J] > 8:
                                ColorAssignment = [2, 1]
                                PoolMsg = 'Player 1 is Blue, Player 2 is Yellow'
                        else:
                            if BallPotSeq[J] < 8:
                                ColorAssignment = [2, 1]
                                PoolMsg = 'Player 1 is Blue, Player 2 is Yellow'
                            elif BallPotSeq[J] > 8:
                                ColorAssignment = [1, 2]
                                PoolMsg = 'Player 1 is Yellow, Player 2 is Blue'
                    else:
                        if ColorAssignment[Player - 1] == 1:
                            if BallPotSeq[J] > 8:
                                Foul = 1;
                                PoolMsg = 'FOUL! Player {0} Potted Opponents Ball'.format(Player)
                        elif ColorAssignment[Player - 1] == 2:
                            if BallPotSeq[J] < 8:
                                Foul = 1
                                PoolMsg = 'FOUL! Player {0} Potted Opponents Ball'.format(Player)

            if ColorAssignment[0] == 1:
                Player1NoBallsRemaining = sum(1 for i in UnpottedBalls if (i > 0) & (i < 8))
                Player2NoBallsRemaining = sum(1 for i in UnpottedBalls if (i > 8))
            #            Player1NoBallsRemaining = [i for i, j in enumerate(UnpottedBalls) if ((j < 8) & (j > 0))]
            #            Player2NoBallsRemaining = [i for i, j in enumerate(UnpottedBalls) if j > 9]
            elif ColorAssignment[0] == 2:
                #            Player1NoBallsRemaining = [i for i, j in enumerate(UnpottedBalls) if j > 9]
                #            Player2NoBallsRemaining = [i for i, j in enumerate(UnpottedBalls) if ((j < 8) & (j > 0))]

                Player1NoBallsRemaining = sum(1 for i in UnpottedBalls if (i > 8))
                Player2NoBallsRemaining = sum(1 for i in UnpottedBalls if (i > 0) & (i < 8))
            else:
                Player1NoBallsRemaining = 7;
                Player2NoBallsRemaining = 7;

            if Player1NoBallsRemaining == 0:
                if ReadyForTheBlack[0] == 0:
                    ReadyForTheBlack[0] = 1;
                    PoolMsg = 'Player 1 is going for the black'
            if Player2NoBallsRemaining == 0:
                if ReadyForTheBlack[1] == 0:
                    ReadyForTheBlack[1] = 1;
                    PoolMsg = 'Player 2 is going for the black'