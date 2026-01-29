import random

from settings import ANIMATION_SPEED, pygame, vector, Z_Layer


class Tooth(pygame.sprite.Sprite):
    def __init__(self, groups, position, collision_sprites, animation_frames):
        super().__init__(groups)
        self.animation_frames = animation_frames
        self.frame_index = 0
        self.image = self.animation_frames[self.frame_index]
        self.rect = self.image.get_frect(topleft=position)
        self.z_index = Z_Layer.MAIN.value
        self.direction = random.choice([-1, 1])
        self.speed = 100
        self.collision_rectangles = [sprite.rect for sprite in collision_sprites]

    def move(self, delta_time):
        self.has_reached_surface_edge()
        self.rect.x += self.direction * self.speed * delta_time

    def has_reached_surface_edge(self):
        # Create tiny invisible rectangles on the Tooth's sides which will be used to detect
        # if he has reached the end of the surface he is moving on.
        surface_rectangle_left = pygame.FRect(self.rect.bottomleft, (-1, 1))
        surface_rectangle_right = pygame.FRect(self.rect.bottomright, (1, 1))
        wall_rectangle = pygame.FRect(
            self.rect.topleft + vector(-1, 0), (self.rect.width + 2, 1)
        )

        # The invisible rectangles will be colliding with the surface until he reaches one of the edges
        reached_left_edge = (
            surface_rectangle_left.collidelist(self.collision_rectangles) < 0
        )
        reached_right_edge = (
            surface_rectangle_right.collidelist(self.collision_rectangles) < 0
        )
        did_hit_wall = wall_rectangle.collidelist(self.collision_rectangles) >= 0

        if (reached_left_edge or did_hit_wall) and self.direction == -1:
            self.direction = 1
        if (reached_right_edge or did_hit_wall) and self.direction == 1:
            self.direction = -1

    def animate(self, delta_time):
        self.frame_index += ANIMATION_SPEED * delta_time
        self.image = self.animation_frames[
            int(self.frame_index % len(self.animation_frames))
        ]
        self.image = (
            pygame.transform.flip(self.image, True, False)
            if self.direction == -1
            else self.image
        )

    def update(self, delta_time):
        self.animate(delta_time)
        self.move(delta_time)
