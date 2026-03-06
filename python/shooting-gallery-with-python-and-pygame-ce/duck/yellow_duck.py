from settings import WINDOW_WIDTH

from .duck import Duck


class YellowDuck(Duck):
    def __init__(self, groups, image, position, has_target):
        super().__init__(groups, image, position)

        self.speed = 1
        self.points = 2 if has_target else 1

    def update(self):
        self.rect.x += self.speed

        if self.rect.x > WINDOW_WIDTH:
            self.kill()
