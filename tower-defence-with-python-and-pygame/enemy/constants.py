# Images paths
ENEMY_1_PATH = "assets/images/enemies/enemy_1.png"
ENEMY_2_PATH = "assets/images/enemies/enemy_2.png"
ENEMY_3_PATH = "assets/images/enemies/enemy_3.png"
ENEMY_4_PATH = "assets/images/enemies/enemy_4.png"

SPAWN_ENEMY_COOLDOWN = 400

# Describes how many enemies of each type will be spawned for a particular level
ENEMY_SPAWN_DATA = [
  {
    # "level": 1,
    "weak": 15,
    "medium": 0,
    "strong": 0,
    "elite": 0
  },
  {
    # "level": 2,
    "weak": 30,
    "medium": 0,
    "strong": 0,
    "elite": 0
  },
  {
    # "level": 3,
    "weak": 20,
    "medium": 5,
    "strong": 0,
    "elite": 0
  },
  {
    # "level": 4,
    "weak": 30,
    "medium": 15,
    "strong": 0,
    "elite": 0
  },
  {
    # "level": 5,
    "weak": 5,
    "medium": 20,
    "strong": 0,
    "elite": 0
  },
  {
    # "level": 6,
    "weak": 15,
    "medium": 15,
    "strong": 4,
    "elite": 0
  },
  {
    # "level": 7,
    "weak": 20,
    "medium": 25,
    "strong": 5,
    "elite": 0
  },
  {
    # "level": 8,
    "weak": 10,
    "medium": 20,
    "strong": 15,
    "elite": 0
  },
  {
    # "level": 9,
    "weak": 15,
    "medium": 10,
    "strong": 5,
    "elite": 0
  },
  {
    # "level": 10,
    "weak": 0,
    "medium": 100,
    "strong": 0,
    "elite": 0
  },
  {
    # "level": 11,
    "weak": 5,
    "medium": 10,
    "strong": 12,
    "elite": 2
  },
  {
    # "level": 12,
    "weak": 0,
    "medium": 15,
    "strong": 10,
    "elite": 5
  },
  {
    # "level": 13,
    "weak": 20,
    "medium": 0,
    "strong": 25,
    "elite": 10
  },
  {
    # "level": 14,
    "weak": 15,
    "medium": 15,
    "strong": 15,
    "elite": 15
  },
  {
    # "level": 15,
    "weak": 25,
    "medium": 25,
    "strong": 25,
    "elite": 25
  }
]

ENEMY_DATA = {
    "weak": {
    "health": 10,
    "speed": 2
  },
    "medium": {
    "health": 15,
    "speed": 3
  },
    "strong": {
    "health": 20,
    "speed": 4
  },
    "elite": {
    "health": 30,
    "speed": 6
  }
}
