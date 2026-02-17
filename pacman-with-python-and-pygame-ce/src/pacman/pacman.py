from levels.constants import BoardTile, TILE_HEIGHT, TILE_WIDTH
from settings import ANIMATION_SPEED, pygame, WINDOW_HEIGHT, WINDOW_WIDTH

from .constants import (
    COLLISION_FUDGE_FACTOR,
    Direction,
    TILE_CENTER_FACTOR_MAX,
    TILE_CENTER_FACTOR_MIN,
)


class PacMan(pygame.sprite.Sprite):
    def __init__(self, groups, animation_frames, position, level_layout):
        super().__init__(groups)

        # We have to scale the original Pacman images, because they are too big
        self.animation_frames = list(
            map(lambda frame: pygame.transform.scale(frame, (45, 45)), animation_frames)
        )
        self.frame_index = 0
        self.position = position
        self.image = self.animation_frames[self.frame_index]
        # Represents a rectangle to figure out where the Pacman will be drawn in a current frame
        self.rect = self.image.get_rect(center=position)
        self.level_layout = level_layout
        self.speed = 10
        self.direction = Direction.RIGHT
        self.direction_command = Direction.RIGHT
        self.allowed_turns = {
            Direction.LEFT: False,
            Direction.RIGHT: False,
            Direction.UP: False,
            Direction.DOWN: False,
        }

    def process_key_input(self):
        pressed_keys = pygame.key.get_pressed()
        released_keys = pygame.key.get_just_released()

        if pressed_keys[pygame.K_LEFT]:
            self.direction_command = Direction.LEFT
        if pressed_keys[pygame.K_RIGHT]:
            self.direction_command = Direction.RIGHT
        if pressed_keys[pygame.K_UP]:
            self.direction_command = Direction.UP
        if pressed_keys[pygame.K_DOWN]:
            self.direction_command = Direction.DOWN

        if (
            released_keys[pygame.K_LEFT]
            and self.direction_command == Direction.LEFT
            or released_keys[pygame.K_RIGHT]
            and self.direction_command == Direction.RIGHT
            or released_keys[pygame.K_UP]
            and self.direction_command == Direction.UP
            or released_keys[pygame.K_DOWN]
            and self.direction_command == Direction.DOWN
        ):
            self.direction_command = self.direction

        if (
            self.direction_command == Direction.LEFT
            and self.allowed_turns[Direction.LEFT]
        ):
            self.direction = Direction.LEFT
        if (
            self.direction_command == Direction.RIGHT
            and self.allowed_turns[Direction.RIGHT]
        ):
            self.direction = Direction.RIGHT
        if self.direction_command == Direction.UP and self.allowed_turns[Direction.UP]:
            self.direction = Direction.UP
        if (
            self.direction_command == Direction.DOWN
            and self.allowed_turns[Direction.DOWN]
        ):
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

    def update_allowed_turns(self):
        # Restart allowed turns
        self.allowed_turns[Direction.LEFT] = False
        self.allowed_turns[Direction.RIGHT] = False
        self.allowed_turns[Direction.UP] = False
        self.allowed_turns[Direction.DOWN] = False

        if (
            self.rect.centerx - self.rect.width / 2 < 0
            or self.rect.centerx + self.rect.width / 2 >= WINDOW_WIDTH
        ):
            self.allowed_turns[Direction.LEFT] = True
            self.allowed_turns[Direction.RIGHT] = True
        else:
            open_tiles = [
                BoardTile.EMPTY_BLACK_RECTANGLE.value,
                BoardTile.DOT.value,
                BoardTile.BIG_DOT.value,
            ]

            if (
                self.direction == Direction.LEFT
                and self.level_layout[self.rect.centery // TILE_HEIGHT][
                    (self.rect.centerx + COLLISION_FUDGE_FACTOR) // TILE_WIDTH
                ]
                in open_tiles
            ):
                self.allowed_turns[Direction.RIGHT] = True
            if (
                self.direction == Direction.RIGHT
                and self.level_layout[self.rect.centery // TILE_HEIGHT][
                    (self.rect.centerx - COLLISION_FUDGE_FACTOR) // TILE_WIDTH
                ]
                in open_tiles
            ):
                self.allowed_turns[Direction.LEFT] = True
            if (
                self.direction == Direction.UP
                and self.level_layout[
                    (self.rect.centery + COLLISION_FUDGE_FACTOR) // TILE_HEIGHT
                ][self.rect.centerx // TILE_WIDTH]
                in open_tiles
            ):
                self.allowed_turns[Direction.DOWN] = True
            if (
                self.direction == Direction.DOWN
                and self.level_layout[
                    (self.rect.centery - COLLISION_FUDGE_FACTOR) // TILE_HEIGHT
                ][(self.rect.centerx) // TILE_WIDTH]
                in open_tiles
            ):
                self.allowed_turns[Direction.UP] = True

            if self.direction in [Direction.UP, Direction.DOWN]:
                if (
                    TILE_CENTER_FACTOR_MIN
                    <= self.rect.centerx % TILE_WIDTH
                    <= TILE_CENTER_FACTOR_MAX
                ):
                    # If the position above the Pacman is open
                    if (
                        self.level_layout[
                            (self.rect.centery - COLLISION_FUDGE_FACTOR) // TILE_HEIGHT
                        ][self.rect.centerx // TILE_WIDTH]
                        in open_tiles
                    ):
                        self.allowed_turns[Direction.UP] = True
                    # If the position below the Pacman is open
                    if (
                        self.level_layout[
                            (self.rect.centery + COLLISION_FUDGE_FACTOR) // TILE_HEIGHT
                        ][self.rect.centerx // TILE_WIDTH]
                        in open_tiles
                    ):
                        self.allowed_turns[Direction.DOWN] = True

                if (
                    TILE_CENTER_FACTOR_MIN
                    <= self.rect.centery % TILE_HEIGHT
                    <= TILE_CENTER_FACTOR_MAX
                ):
                    if (
                        self.level_layout[self.rect.centery // TILE_HEIGHT][
                            (self.rect.centerx - TILE_WIDTH) // TILE_WIDTH
                        ]
                        in open_tiles
                    ):
                        self.allowed_turns[Direction.LEFT] = True
                    if (
                        self.level_layout[self.rect.centery // TILE_HEIGHT][
                            (self.rect.centerx + TILE_WIDTH) // TILE_WIDTH
                        ]
                        in open_tiles
                    ):
                        self.allowed_turns[Direction.RIGHT] = True

            if self.direction in [Direction.LEFT, Direction.RIGHT]:
                if (
                    TILE_CENTER_FACTOR_MIN
                    <= self.rect.centerx % TILE_WIDTH
                    <= TILE_CENTER_FACTOR_MAX
                ):
                    # If the position above the Pacman is open
                    if (
                        self.level_layout[
                            (self.rect.centery - TILE_HEIGHT) // TILE_HEIGHT
                        ][self.rect.centerx // TILE_WIDTH]
                        in open_tiles
                    ):
                        self.allowed_turns[Direction.UP] = True
                    # If the position below the Pacman is open
                    if (
                        self.level_layout[
                            (self.rect.centery + TILE_HEIGHT) // TILE_HEIGHT
                        ][self.rect.centerx // TILE_WIDTH]
                        in open_tiles
                    ):
                        self.allowed_turns[Direction.DOWN] = True

                if (
                    TILE_CENTER_FACTOR_MIN
                    <= self.rect.centery % TILE_HEIGHT
                    <= TILE_CENTER_FACTOR_MAX
                ):
                    if (
                        self.level_layout[self.rect.centery // TILE_HEIGHT][
                            (self.rect.centerx + COLLISION_FUDGE_FACTOR) // TILE_WIDTH
                        ]
                        in open_tiles
                    ):
                        self.allowed_turns[Direction.RIGHT] = True
                    if (
                        self.level_layout[self.rect.centery // TILE_HEIGHT][
                            (self.rect.centerx - COLLISION_FUDGE_FACTOR) // TILE_WIDTH
                        ]
                        in open_tiles
                    ):
                        self.allowed_turns[Direction.LEFT] = True

    def move(self, delta_time):
        if self.direction == Direction.LEFT and self.allowed_turns[Direction.LEFT]:
            self.rect.centerx -= self.speed * delta_time
        if self.direction == Direction.RIGHT and self.allowed_turns[Direction.RIGHT]:
            self.rect.centerx += self.speed * delta_time
        if self.direction == Direction.UP and self.allowed_turns[Direction.UP]:
            self.rect.centery -= self.speed * delta_time
        if self.direction == Direction.DOWN and self.allowed_turns[Direction.DOWN]:
            self.rect.centery += self.speed * delta_time

        if self.rect.centerx > WINDOW_WIDTH:
            self.rect.centerx = -47
        elif self.rect.centerx - self.rect.width / 2 < 0:
            self.rect.centerx = WINDOW_WIDTH - 3

    def update(self, delta_time):
        self.update_allowed_turns()
        self.process_key_input()
        self.animate(delta_time)
        self.move(delta_time)
