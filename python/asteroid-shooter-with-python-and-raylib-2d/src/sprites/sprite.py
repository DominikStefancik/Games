from settings import draw_texture_v, Vector2, WHITE, WINDOW_HEIGHT

from .constants import SPRITE_REMOVE_THRESHOLD


class Sprite:
    def __init__(self, group, texture, position, speed, direction):
        self.texture = texture
        self.position = position
        self.speed = speed
        self.direction = direction
        self.size = Vector2(texture.width, texture.height)
        self.to_be_removed = False

        # For a collision detection, we will not use rectangle derived from the Sprite's texture,
        # but rather a circle with the center where the texture's center is
        self.collision_radius = self.size.y / 2

        group.append(self)

    def get_center(self):
        return Vector2(
            self.position.x + self.size.x / 2, self.position.y + self.size.y / 2
        )

    def move(self, delta_time):
        self.position.x += self.direction.x * self.speed * delta_time
        self.position.y += self.direction.y * self.speed * delta_time

    def check_to_be_removed(self):
        self.to_be_removed = (
            -SPRITE_REMOVE_THRESHOLD > self.position.y
            or self.position.y > (WINDOW_HEIGHT + SPRITE_REMOVE_THRESHOLD)
        )

    def update(self, delta_time):
        self.move(delta_time)
        self.check_to_be_removed()

    def draw(self):
        draw_texture_v(self.texture, self.position, WHITE)
