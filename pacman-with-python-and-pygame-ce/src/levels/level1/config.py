from settings import Direction

LEVEL_1_CONFIG = {
    "wall_color": "blue",
    "gate_color": "white",
    "dot_color": "white",
    "dot_score": 10,
    "big_dot_score": 50,
    "pacman": {"position": (450, 663), "direction": Direction.RIGHT, "speed": 1},
    "blinky": {
        "position": (78, 78),
        "direction": Direction.RIGHT,
        "target": (450, 663),
        "speed": 1,
        "is_in_box": False,
    },
    "inky": {
        "position": (440, 388),
        "direction": Direction.UP,
        "target": (450, 663),
        "speed": 1,
        "is_in_box": False,
    },
    "pinky": {
        "position": (440, 438),
        "direction": Direction.UP,
        "target": (450, 663),
        "speed": 1,
        "is_in_box": False,
    },
    "clyde": {
        "position": (440, 438),
        "direction": Direction.UP,
        "target": (450, 663),
        "speed": 1,
        "is_in_box": False,
    },
}
