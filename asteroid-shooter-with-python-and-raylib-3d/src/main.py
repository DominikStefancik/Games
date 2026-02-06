from settings import (
    BACKGROUND_COLOR,
    begin_drawing,
    clear_background,
    close_window,
    end_drawing,
    init_window,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    window_should_close,
)


class Game:
    def __init__(self):
        # The "init_window" function is imported from "settings.py" where there is "from pyray import *" statement
        init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Python Asteroid Shooter 3D")

    def update(self):
        pass

    def draw(self):
        begin_drawing()
        clear_background(BACKGROUND_COLOR)
        end_drawing()

    def run(self):
        while not window_should_close():
            self.update()
            self.draw()

        close_window()


# To make sure we are running only main.py and not anything else
if __name__ == "__main__":
    game = Game()
    game.run()
