from .duck import Duck


class BrownDuck(Duck):
    def __init__(self, groups, image, position, has_target):
        super().__init__(groups, image, position)

        self.speed = 2
        self.points = 4 if has_target else 2

    def update(self):
        self.rect.x -= self.speed

        if self.rect.right < 0:
            self.kill()
