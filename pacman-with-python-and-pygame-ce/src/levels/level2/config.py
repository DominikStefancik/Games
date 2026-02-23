from settings import Direction, Vector2

LEVEL_2_CONFIG = {
    "color": {"wall": "purple", "gate": "yellow", "dot": "white", "big_dot": "red"},
    "score_points": {"dot": 10, "big_dot": 50, "ghost": 200},
    "ghost_box": {
        "top_left": Vector2(350, 370),
        "bottom_right": Vector2(550, 470),
        "target_position": Vector2(420, 420),
    },
    "pacman": {"position": (450, 663), "direction": Direction.RIGHT, "speed": 1},
    "blinky": {
        "position": (78, 78),
        "direction": Direction.RIGHT,
        "speed": {"normal": 1, "power_up": 1, "dead": 2},
        "is_in_box": False,
    },
    "inky": {
        "position": (820, 820),
        "direction": Direction.LEFT,
        "speed": {"normal": 1, "power_up": 1, "dead": 2},
        "is_in_box": False,
    },
    "pinky": {
        "position": (420, 418),
        "direction": Direction.UP,
        "speed": {"normal": 1, "power_up": 1, "dead": 2},
        "is_in_box": False,
    },
    "clyde": {
        "position": (480, 418),
        "direction": Direction.UP,
        "speed": {"normal": 1, "power_up": 1, "dead": 2},
        "is_in_box": False,
    },
}
