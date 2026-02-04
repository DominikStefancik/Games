from random import randint, uniform

from settings import Vector2, WINDOW_HEIGHT, WINDOW_WIDTH


def create_stars_data():
    return [
        (
            Vector2(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)), # position
            uniform(0.5, 1.8) # size
        ) for index in range(25)
    ]
