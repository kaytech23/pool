import player


class ManualPlayer(player.Player):

    def game_init(self, balls):
        pass

    def simulation_finish(self, game_state, player, balls, foul, color_assignment):
        pass

    def simulation_start(self, player, balls):
        pass

    def get_cueball_position(self):
        return 100, 100

    def get_stroke(self):
        return 1.32, 24000

    def on_key_press(self, symbol):
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def update(self, df):
        pass

