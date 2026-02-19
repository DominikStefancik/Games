from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import AudioAsset
from game_state.game_state_manager import get_game_state_manager
from levels.constants import (
    BoardTile,
    COLLISION_FUDGE_FACTOR,
    TILE_CENTER_FACTOR_MAX,
    TILE_CENTER_FACTOR_MIN,
    TILE_HEIGHT,
    TILE_WIDTH,
)
from settings import ANIMATION_SPEED, Direction, pygame, WINDOW_HEIGHT, WINDOW_WIDTH
from timers.timers_manager import get_timers_manager


class PacMan(pygame.sprite.Sprite):
    def __init__(self, groups, animation_frames):
        super().__init__(groups)

        self.game_state_manager = get_game_state_manager()
        self.pacman_config = self.game_state_manager.get_level_config()["pacman"]
        level_layout = self.game_state_manager.get_level_layout()
        position = self.pacman_config["position"]

        # We have to scale the original Pacman images, because they are too big
        self.animation_frames = list(
            map(lambda frame: pygame.transform.scale(frame, (45, 45)), animation_frames)
        )
        self.frame_index = 0
        self.image = self.animation_frames[self.frame_index]
        # Represents a rectangle to figure out where the Pacman will be drawn in a current frame
        self.rect = self.image.get_rect(center=position)
        self.level_layout = level_layout
        self.direction = self.pacman_config["direction"]
        self.direction_command = self.direction
        self.speed = self.pacman_config["speed"]
        self.allowed_turns = {
            Direction.LEFT: False,
            Direction.RIGHT: False,
            Direction.UP: False,
            Direction.DOWN: False,
        }

        self.game_state_manager.subscribe(self)

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
            tile_left = self.level_layout[self.rect.centery // TILE_HEIGHT][
                (self.rect.centerx - COLLISION_FUDGE_FACTOR) // TILE_WIDTH
            ]
            tile_right = self.level_layout[self.rect.centery // TILE_HEIGHT][
                (self.rect.centerx + COLLISION_FUDGE_FACTOR) // TILE_WIDTH
            ]
            tile_up = self.level_layout[
                (self.rect.centery - COLLISION_FUDGE_FACTOR) // TILE_HEIGHT
            ][self.rect.centerx // TILE_WIDTH]
            tile_down = self.level_layout[
                (self.rect.centery + COLLISION_FUDGE_FACTOR) // TILE_HEIGHT
            ][self.rect.centerx // TILE_WIDTH]

            open_tiles = [
                BoardTile.EMPTY_BLACK_RECTANGLE.value,
                BoardTile.DOT.value,
                BoardTile.BIG_DOT.value,
            ]

            if self.direction == Direction.LEFT and tile_right in open_tiles:
                self.allowed_turns[Direction.RIGHT] = True

            if self.direction == Direction.RIGHT and tile_left in open_tiles:
                self.allowed_turns[Direction.LEFT] = True

            if self.direction == Direction.UP and tile_down in open_tiles:
                self.allowed_turns[Direction.DOWN] = True

            if self.direction == Direction.DOWN and tile_up in open_tiles:
                self.allowed_turns[Direction.UP] = True

            if self.direction in [Direction.UP, Direction.DOWN]:
                # Check if the current position is moderately in the center of a tile
                if (
                    TILE_CENTER_FACTOR_MIN
                    <= self.rect.centerx % TILE_WIDTH
                    <= TILE_CENTER_FACTOR_MAX
                ):
                    # If the position above the Pacman is open
                    if tile_up in open_tiles:
                        self.allowed_turns[Direction.UP] = True

                    # If the position below the Pacman is open
                    if tile_down in open_tiles:
                        self.allowed_turns[Direction.DOWN] = True

                if (
                    TILE_CENTER_FACTOR_MIN
                    <= self.rect.centery % TILE_HEIGHT
                    <= TILE_CENTER_FACTOR_MAX
                ):
                    tile_left = self.level_layout[self.rect.centery // TILE_HEIGHT][
                        (self.rect.centerx - TILE_WIDTH) // TILE_WIDTH
                    ]
                    tile_right = self.level_layout[self.rect.centery // TILE_HEIGHT][
                        (self.rect.centerx + TILE_WIDTH) // TILE_WIDTH
                    ]

                    if tile_left in open_tiles:
                        self.allowed_turns[Direction.LEFT] = True

                    if tile_right in open_tiles:
                        self.allowed_turns[Direction.RIGHT] = True

            if self.direction in [Direction.LEFT, Direction.RIGHT]:
                if (
                    TILE_CENTER_FACTOR_MIN
                    <= self.rect.centerx % TILE_WIDTH
                    <= TILE_CENTER_FACTOR_MAX
                ):
                    tile_up = self.level_layout[
                        (self.rect.centery - TILE_HEIGHT) // TILE_HEIGHT
                    ][self.rect.centerx // TILE_WIDTH]
                    tile_down = self.level_layout[
                        (self.rect.centery + TILE_HEIGHT) // TILE_HEIGHT
                    ][self.rect.centerx // TILE_WIDTH]

                    # If the position above the Pacman is open
                    if tile_up in open_tiles:
                        self.allowed_turns[Direction.UP] = True

                    # If the position below the Pacman is open
                    if tile_down in open_tiles:
                        self.allowed_turns[Direction.DOWN] = True

                if (
                    TILE_CENTER_FACTOR_MIN
                    <= self.rect.centery % TILE_HEIGHT
                    <= TILE_CENTER_FACTOR_MAX
                ):
                    if tile_right in open_tiles:
                        self.allowed_turns[Direction.RIGHT] = True

                    if tile_left in open_tiles:
                        self.allowed_turns[Direction.LEFT] = True

    def detect_collisions(self):
        # We have to avoid checking the collisions when the Pacman is on the left of right edge of the screen
        # (for the case when he goes out of the right edge and pops up on the left edge, and vice versa).
        # Otherwise we will get out of index range exception in that case.
        if 0 < self.rect.centerx < WINDOW_WIDTH - TILE_WIDTH:
            tile = self.level_layout[self.rect.centery // TILE_HEIGHT][
                self.rect.centerx // TILE_WIDTH
            ]
            is_tile_dot = False

            asset_manager = get_asset_manager()
            if tile == BoardTile.DOT.value:
                self.game_state_manager.score += (
                    self.game_state_manager.get_level_config()["score_points"]["dot"]
                )
                is_tile_dot = True
                asset_manager.sounds[AudioAsset.EAT_DOT].play()

            if tile == BoardTile.BIG_DOT.value:
                self.game_state_manager.score += (
                    self.game_state_manager.get_level_config()["score_points"][
                        "big_dot"
                    ]
                )
                is_tile_dot = True
                timers_manager = get_timers_manager()
                timers_manager.power_up_timer.activate()
                asset_manager.sounds[AudioAsset.EAT_BIG_DOT].play()
                asset_manager.sounds[AudioAsset.POWER_UP].play()

            if is_tile_dot:
                self.level_layout[self.rect.centery // TILE_HEIGHT][
                    self.rect.centerx // TILE_WIDTH
                ] = BoardTile.EMPTY_BLACK_RECTANGLE.value

    def restart(self):
        self.frame_index = 0
        self.image = self.animation_frames[self.frame_index]

        position = self.pacman_config["position"]
        # Represents a rectangle to figure out where the Pacman will be drawn in a current frame
        self.rect = self.image.get_rect(center=position)
        self.direction = self.pacman_config["direction"]
        self.direction_command = self.direction

    def update_state(self):
        self.restart()

    def move(self):
        if self.direction == Direction.LEFT and self.allowed_turns[Direction.LEFT]:
            self.rect.centerx -= self.speed
        if self.direction == Direction.RIGHT and self.allowed_turns[Direction.RIGHT]:
            self.rect.centerx += self.speed
        if self.direction == Direction.UP and self.allowed_turns[Direction.UP]:
            self.rect.centery -= self.speed
        if self.direction == Direction.DOWN and self.allowed_turns[Direction.DOWN]:
            self.rect.centery += self.speed

        if self.rect.centerx > WINDOW_WIDTH + self.rect.width / 4:
            self.rect.centerx = -self.rect.width / 4
        elif self.rect.centerx < -self.rect.width / 4:
            self.rect.centerx = WINDOW_WIDTH + self.rect.width / 4

    def update(self, delta_time):
        self.update_allowed_turns()
        self.process_key_input()
        self.animate(delta_time)
        self.move()
        self.detect_collisions()
