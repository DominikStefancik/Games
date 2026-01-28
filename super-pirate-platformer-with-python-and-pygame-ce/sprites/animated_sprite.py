from settings import ANIMATION_SPEED

from .constants import MovingDirection
from .sprite import Sprite


class AnimatedSprite(Sprite):
    def __init__(
        self, groups, position, animation_frames, animation_speed=ANIMATION_SPEED
    ):
        self.frames = animation_frames
        self.frame_index = 0
        super().__init__(groups, self.frames[self.frame_index], position)
        self.animation_speed = animation_speed

    def animate(self, delta_time):
        self.frame_index += self.animation_speed * delta_time
        # Using "self.frame_index % len(self.frames)" is the same as checking "self.frame_index >= len(self.frames)"
        self.image = self.frames[int(self.frame_index % len(self.frames))]

    def update(self, delta_time):
        self.animate(delta_time)
