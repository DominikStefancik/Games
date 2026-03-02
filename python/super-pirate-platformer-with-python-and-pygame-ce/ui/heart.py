from random import randint
from settings import ANIMATION_SPEED
from sprites.animated_sprite import AnimatedSprite

class Heart(AnimatedSprite):
    def __init__(self, groups, position, animation_frames):
        super().__init__(groups, position, animation_frames)

        self.is_animation_active = False

    def animate(self, delta_time):
        self.frame_index += ANIMATION_SPEED * delta_time

        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.is_animation_active = False
            self.frame_index = 0

    def update(self, delta_time):
        if self.is_animation_active:
            self.animate(delta_time)
        else:
            # Using random number generator to simulate a timer
            self.is_animation_active = randint(0, 2000) == 1
