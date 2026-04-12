from enum import Enum


class ImageAsset(Enum):
    TABLE = "table"
    BALL_1 = "ball_1"
    BALL_2 = "ball_2"
    BALL_3 = "ball_3"
    BALL_4 = "ball_4"
    BALL_5 = "ball_5"
    BALL_6 = "ball_6"
    BALL_7 = "ball_7"
    BALL_8 = "ball_8"
    BALL_9 = "ball_9"
    BALL_10 = "ball_10"
    BALL_11 = "ball_11"
    BALL_12 = "ball_12"
    BALL_13 = "ball_13"
    BALL_14 = "ball_14"
    BALL_15 = "ball_15"
    CUE_BALL = "cue_ball"

    @staticmethod
    def get_ball(index):
        match index:
            case 1:
                return ImageAsset.BALL_1
            case 2:
                return ImageAsset.BALL_2
            case 3:
                return ImageAsset.BALL_3
            case 4:
                return ImageAsset.BALL_4
            case 5:
                return ImageAsset.BALL_5
            case 6:
                return ImageAsset.BALL_6
            case 7:
                return ImageAsset.BALL_7
            case 8:
                return ImageAsset.BALL_8
            case 9:
                return ImageAsset.BALL_9
            case 10:
                return ImageAsset.BALL_10
            case 11:
                return ImageAsset.BALL_11
            case 12:
                return ImageAsset.BALL_12
            case 13:
                return ImageAsset.BALL_13
            case 14:
                return ImageAsset.BALL_14
            case 15:
                return ImageAsset.BALL_15
            case _:
                raise NotImplementedError


class FontAsset(Enum):
    FONT = "font"


class AudioAsset(Enum):
    SOUND = "sound"
