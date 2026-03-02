from enum import Enum


class EnemyType(Enum):
    WEAK = "weak",
    MEDIUM = "medium",
    STRONG = "strong",
    ELITE = "elite"

    @staticmethod
    def from_str(label):
        if label == "weak":
            return EnemyType.WEAK
        elif label == "medium":
            return EnemyType.MEDIUM
        elif label == "strong":
            return EnemyType.STRONG
        elif label == "elite":
            return EnemyType.ELITE
        else:
            raise NotImplementedError

    def __str__(self):
        if self == EnemyType.WEAK:
            return "weak"
        elif self == EnemyType.MEDIUM:
            return "medium"
        elif self == EnemyType.STRONG:
            return "strong"
        elif self == EnemyType.ELITE:
            return "elite"
        else:
            raise NotImplementedError
