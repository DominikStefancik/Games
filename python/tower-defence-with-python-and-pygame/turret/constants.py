from os.path import join

# Images paths
CURSOR_TURRET_PATH = join("assets", "images", "turrets", "cursor_turret.png")
BUY_TURRET_PATH = join("assets", "images", "buttons", "buy_turret.png")
UPGRADE_TURRET_PATH = join("assets", "images", "buttons", "upgrade_turret.png")
CANCEL_PATH = join("assets", "images", "buttons", "cancel.png")

# Audio paths
SHOT_SOUND_PATH = join("assets", "audio", "shot.wav")


TURRET_ANIMATION_FRAMES = 8
TURRET_ANIMATION_STEP_INTERVAL = 15

TURRET_DATA = [
    {
        "upgrade_level": 1,
        "range": 90,
        "cooldown_interval": 1500
    },
    {
        "upgrade_level": 2,
        "range": 110,
        "cooldown_interval": 1200
    },
    {
        "upgrade_level": 3,
        "range": 125,
        "cooldown_interval": 1000
    },
    {
        "upgrade_level": 4,
        "range": 150,
        "cooldown_interval": 900
    }
]

BUY_TURRET_COST = 120
UPGRADE_TURRET_COST = 100
KILL_ENEMY_REWARD = 1

TURRET_DAMAGE = 5
