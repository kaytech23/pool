class GameWorld(object):

    def __init__(self, player1, player2):

        self.player1 = player1
        self.player2 = player2

    # players state ?
    # current players
    # pocketed balls
    # f0ul
    # game state: init, play, gameover

    # game_play states: get_cueball_position, wait, get_player_hit, simulate

    # balls positions
    # cue ball
    # color_balls
    # black_ball

    player updates
    player.initstate(balls)



    def play_full_game(self):
        init_game()
        state = game_play
        while game_play
            if foul:
                cue_ball_position = current_player.get_foul_cueball_position()
                pool_simulator.update_cueball(cue_ball_position)
            angle, force = current_player.get_player_move()
            pool_simulator.set_cueball_hit(angle, force)
            pool_simulator.full_update()
            check_results()

    def play_interactive_game(self):
        init_game()

    def interactive_update(self, delta_time):
        if game_init
            pass
        elif game_play:
            if get_cueball_position:
                changestate -> wait
                new thread()
                    cue_ball_position = current_player.get_foul_cueball_position()
                    pool_simulator.update_cueball(cue_ball_position)
                    state = get_player_hit
            if wait:
                pass
            if get_player_hit
                changestate -> wait
                new thread()
                    angle, force = current_player.get_player_move()
                    pool_simulator.set_cueball_hit(angle, force)
                    state = simulate
            if simulate:
                is_done = pool_simulator.update(delta_time)
                if (is_done):
                    checkresults()
                    if foul:
                        state = get_player_cueball_position
                    else
                        state = get_player_hit
        elif game_over:
            pass



    pass

