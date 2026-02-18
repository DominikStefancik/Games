from settings import Direction, Vector2

LEVEL_1_CONFIG = {
    "wall_color": "blue",
    "gate_color": "white",
    "dot_color": "white",
    "dot_score": 10,
    "big_dot_score": 50,
    "ghost_box_position": Vector2(380, 400),
    "pacman": {"position": (450, 663), "direction": Direction.RIGHT, "speed": 1},
    "blinky": {
        "position": (78, 78),
        "direction": Direction.RIGHT,
        "speed": 1,
        "is_in_box": False,
    },
    "inky": {
        "position": (440, 388),
        "direction": Direction.UP,
        "speed": 1,
        "is_in_box": False,
    },
    "pinky": {
        "position": (440, 438),
        "direction": Direction.UP,
        "speed": 1,
        "is_in_box": False,
    },
    "clyde": {
        "position": (440, 438),
        "direction": Direction.UP,
        "speed": 1,
        "is_in_box": False,
    },
}
