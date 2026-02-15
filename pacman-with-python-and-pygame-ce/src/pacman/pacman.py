from settings import ANIMATION_SPEED, pygame

from .constants import Direction


class PacMan(pygame.sprite.Sprite):
    def __init__(self, groups, animation_frames, position):
        super().__init__(groups)

        # We have to scale the original Pacman images, because they are too big
        self.animation_frames = list(
            map(lambda frame: pygame.transform.scale(frame, (45, 45)), animation_frames)
        )
        self.frame_index = 0
        self.position = position
        self.image = self.animation_frames[self.frame_index]
        # Represents a rectangle to figure out where the Pacman will be drawn in a current frame
        self.rect = self.image.get_frect(center=position)
        self.direction = Direction.RIGHT

    def process_key_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.direction = Direction.LEFT
        if keys[pygame.K_RIGHT]:
            self.direction = Direction.RIGHT
        if keys[pygame.K_UP]:
            self.direction = Direction.UP
        if keys[pygame.K_DOWN]:
            self.direction = Direction.DOWN

    def animate(self, delta_time):
        self.frame_index += ANIMATION_SPEED * delta_time

        self.image = self.animation_frames[
            int(self.frame_index % len(self.animation_frames))
        ]

        match self.direction:
            case Direction.LEFT:
                self.image = pygame.transform.flip(self.image, True, False)
            case Direction.UP:
                self.image = pygame.transform.rotate(self.image, 90)
            case Direction.DOWN:
                self.image = pygame.transform.rotate(self.image, -90)

    def update(self, delta_time):
        self.process_key_input()
        self.animate(delta_time)
