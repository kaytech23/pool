

class Player:

    def reset_cue_ball_position(self):
        return 100, 100

    def get_stroke(self):
        return 1.32, 24000

    def new_game(self, balls_state):
        pass

    def simulation_update(self, balls_state, balls_pocketed, simulation_state):
        pass

    def cue_ball_position_update(self, x, y):
        pass

    def opponent_simulation_update(self, balls_state, balls_pocketed, simulation_state):
        pass

    def opponent_cue_ball_position_update(self, x, y):
        pass

    def color_assignment_update(self, color_assignment):
        pass

    def keystroke_hit(self, key):
        pass

    def mouse_event(self, mouse_event):
        pass

    def update(self, df):
        pass
