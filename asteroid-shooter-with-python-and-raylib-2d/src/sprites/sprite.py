from settings import draw_texture_v, Vector2, WHITE


class Sprite:
    def __init__(self, texture, position, speed, direction):
        self.texture = texture
        self.position = position
        self.speed = speed
        self.direction = direction
        self.size = Vector2(texture.width, texture.height)

    def move(self, delta_time):
        self.position.x += self.direction.x * self.speed * delta_time
        self.position.y += self.direction.y * self.speed * delta_time

    def update(self, delta_time):
        pass

    def draw(self):
        draw_texture_v(self.texture, self.position, WHITE)
