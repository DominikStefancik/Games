from settings import draw_model, Vector3, WHITE


class Model:
    def __init__(self, group, model, position, speed, direction=Vector3()):
        self.model = model
        self.position = position
        self.speed = speed
        self.direction = direction
        self.to_be_removed = False

        group.append(self)

    def move(self, delta_time):
        self.position.x += self.direction.x * self.speed * delta_time
        self.position.y += self.direction.y * self.speed * delta_time
        self.position.z += self.direction.z * self.speed * delta_time

    def update(self, delta_time):
        self.move(delta_time)

    def draw(self):
        draw_model(self.model, self.position, 1, WHITE)
