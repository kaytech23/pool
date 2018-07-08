import pool2


class Player(object):

    def init(self):
        pass

    def get_stroke(self):
        return 1.3, 12000

    def get_stroke_after_foul(self):
        return 1, 1, 1.3, 12000

    def simulation_results(self, balls):
        pass

    def opponent_cueball_setup_after_foul(self, x, y):
        pass

    def opponent_simulation_results(self, balls):
        pass

    def on_key_press(self, symbol):
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        pass