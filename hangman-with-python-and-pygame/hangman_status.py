from enum import Enum


class HangmanStatus(Enum):
    EMPTY_ROPE = 0
    HEAD = 1
    TORSO = 2
    ONE_HAND = 3
    BOTH_HANDS = 4
    ONE_LEG = 5
    BOTH_LEGS = 6


    @staticmethod
    def from_int(number):
        if number == 0:
            return HangmanStatus.EMPTY_ROPE
        elif number == 1:
            return HangmanStatus.HEAD
        elif number == 2:
            return HangmanStatus.TORSO
        elif number == 3:
            return HangmanStatus.ONE_HAND
        elif number == 4:
            return HangmanStatus.BOTH_HANDS
        elif number == 5:
            return HangmanStatus.ONE_LEG
        elif number == 6:
            return HangmanStatus.BOTH_LEGS
        else:
            raise NotImplementedError

    def __int__(self):
        if self == HangmanStatus.EMPTY_ROPE:
            return 0
        elif self == HangmanStatus.HEAD:
            return 1
        elif self == HangmanStatus.TORSO:
            return 2
        elif self == HangmanStatus.ONE_HAND:
            return 3
        elif self == HangmanStatus.BOTH_HANDS:
            return 4
        elif self == HangmanStatus.ONE_LEG:
            return 5
        elif self == HangmanStatus.BOTH_LEGS:
            return 6
        else:
            raise NotImplementedError
