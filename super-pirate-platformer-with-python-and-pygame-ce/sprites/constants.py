from enum import Enum

class MovingDirection(Enum):
    VERTICAL = "vertical",
    HORIZONTAL = "horizontal"


class ItemType(Enum):
    DIAMOND = "diamond"
    GOLD = "gold"
    POTION = "potion"
    SILVER = "silver"
    SKULL = "skull"

    @staticmethod
    def from_str(label):
        if label == "diamond":
            return ItemType.DIAMOND
        elif label == "gold":
            return ItemType.GOLD
        elif label == "potion":
            return ItemType.POTION
        elif label == "silver":
            return ItemType.SILVER
        elif label == "skull":
            return ItemType.SKULL
        else:
            raise NotImplementedError
