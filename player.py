from abc import abstractmethod, ABC


class Player(ABC):

    @abstractmethod
    def game_init(self, balls):
        pass

    @abstractmethod
    def simulation_finish(self, game_state, player, balls, foul, color_assignment):
        pass

    @abstractmethod
    def simulation_start(self, player, balls):
        pass

    @abstractmethod
    def get_cueball_position(self):
        return 100, 100

    @abstractmethod
    def get_stroke(self):
        return 1.32, 24000

    @abstractmethod
    def on_key_press(self, symbol, modifiers):
        pass

    @abstractmethod
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    @abstractmethod
    def on_mouse_press(self, x, y, button, modifiers):
        pass

    @abstractmethod
    def update(self, df):
        pass
