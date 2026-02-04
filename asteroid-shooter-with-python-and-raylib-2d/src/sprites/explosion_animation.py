from settings import draw_texture_v, Vector2, WHITE

from .constants import ASTEROID_EXPLOSION_ANIMATION_SPEED


class ExplosionAnimation:
    def __init__(self, textures, position):
        self.textures = textures
        self.textures_index = 0
        self.size = Vector2(self.textures[0].width, self.textures[0].height)
        self.position = Vector2(
            position.x - self.size.x / 2, position.y - self.size.y / 2
        )
        self.to_be_removed = False

    def draw(self):
        draw_texture_v(self.textures[int(self.textures_index)], self.position, WHITE)

    def update(self, delta_time):
        # Play the animation once and then remove the sprite
        if self.textures_index < len(self.textures) - 1:
            self.textures_index += ASTEROID_EXPLOSION_ANIMATION_SPEED * delta_time
        else:
            self.to_be_removed = True
