from enum import Enum


class ShellAnimation(Enum):
    IDLE = "idle"
    FIRE = "fire"


class PearlTimerType(Enum):
    LIFETIME = "lifetime"
    REVERSE = "reverse"
