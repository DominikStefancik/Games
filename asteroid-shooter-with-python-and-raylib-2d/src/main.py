from settings import (
    begin_drawing,
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
        init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Python Asteroid Shooter 2D")

    def run(self):
        while not window_should_close():
            begin_drawing()
            end_drawing()

        close_window()


# To make sure we are running only main.py and not anything else
if __name__ == "__main__":
    game = Game()
    game.run()
