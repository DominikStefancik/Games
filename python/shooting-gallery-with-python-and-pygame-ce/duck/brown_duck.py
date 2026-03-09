from game_state.game_state_manager import get_game_state_manager

from .duck import Duck


class BrownDuck(Duck):
    def __init__(self, group, image, position, has_target):
        super().__init__(group, image, position)

        self.game_state_manager = get_game_state_manager()
        self.speed = 2.5
        self.points = 4 if has_target else 2

    def update(self):
        self.rect.x -= self.speed * self.game_state_manager.round_difficulty

        if self.rect.right < 0:
            self.kill()
