from game_state.game_state_manager import get_game_state_manager
from settings import WINDOW_WIDTH

from .duck import Duck


class YellowDuck(Duck):
    def __init__(self, groups, image, position, has_target):
        super().__init__(groups, image, position)

        self.game_state_manager = get_game_state_manager()
        self.speed = 1
        self.points = 2 if has_target else 1

    def update(self):
        self.rect.x += self.speed * self.game_state_manager.level_difficulty

        if self.rect.x > WINDOW_WIDTH:
            self.kill()
