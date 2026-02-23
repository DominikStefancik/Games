from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import AudioAsset
from game_state.game_state import GameState
from game_state.game_state_manager import get_game_state_manager
from levels.constants import (
    BoardTile,
    COLLISION_FUDGE_FACTOR,
    TILE_CENTER_FACTOR_MAX,
    TILE_CENTER_FACTOR_MIN,
    TILE_HEIGHT,
    TILE_WIDTH,
)
from settings import Direction, pygame, Vector2, WINDOW_HEIGHT, WINDOW_WIDTH
from timers.timers_manager import get_timers_manager

from .constants import GhostImageType, GhostType
from .helpers import (
    get_ghost_images,
    move_blinky,
    move_inky,
    move_pinky,
    move_towards_target,
)


class Ghost(pygame.sprite.Sprite):
    def __init__(self, groups, type, pacman):
        super().__init__(groups)

        self.type = type
        self.pacman = pacman

        self.asset_manager = get_asset_manager()
        self.game_state_manager = get_game_state_manager()
        self.ghost_config = self.game_state_manager.get_level_config()[self.type.value]
        level_layout = self.game_state_manager.get_level_layout()
        self.ghost_box = self.game_state_manager.get_level_config()["ghost_box"]

        self.possible_images = get_ghost_images(self.type)
        self.image = self.possible_images[GhostImageType.MAIN]

        position = self.ghost_config["position"]
        # Represents a rectangle to figure out where the ghost will be drawn in a current frame
        self.rect = self.image.get_rect(center=position)

        self.level_layout = level_layout
        self.direction = self.ghost_config["direction"]
        self.speed = self.ghost_config["speed"]["normal"]
        self.is_in_box = self.ghost_config["is_in_box"]
        self.target_position = self.pacman.rect
        self.is_dead = False
        self.allowed_turns = {
            Direction.LEFT: False,
            Direction.RIGHT: False,
            Direction.UP: False,
            Direction.DOWN: False,
        }

        self.timers_manager = get_timers_manager()

    def update_image(self):
        if not self.timers_manager.power_up_timer.active and not self.is_dead:
            self.image = self.possible_images[GhostImageType.MAIN]
        elif self.timers_manager.power_up_timer.active and not self.is_dead:
            self.image = self.possible_images[GhostImageType.SPOOKED]
        else:
            self.image = self.possible_images[GhostImageType.DEAD]

        self.rect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery))

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

            can_go_through_gate = lambda tile: (
                tile == BoardTile.GATE.value and (self.is_in_box or self.is_dead)
            )

            open_tiles = [
                BoardTile.EMPTY_BLACK_RECTANGLE.value,
                BoardTile.DOT.value,
                BoardTile.BIG_DOT.value,
            ]

            if tile_left in open_tiles or can_go_through_gate(tile_left):
                self.allowed_turns[Direction.LEFT] = True

            if tile_right in open_tiles or can_go_through_gate(tile_right):
                self.allowed_turns[Direction.RIGHT] = True

            if tile_up in open_tiles or can_go_through_gate(tile_up):
                self.allowed_turns[Direction.UP] = True

            if tile_down in open_tiles or can_go_through_gate(tile_down):
                self.allowed_turns[Direction.DOWN] = True

            if self.direction in [Direction.UP, Direction.DOWN]:
                # Check if the current position is moderately in the center of a tile
                if (
                    TILE_CENTER_FACTOR_MIN
                    <= self.rect.centerx % TILE_WIDTH
                    <= TILE_CENTER_FACTOR_MAX
                ):
                    # If the position above the ghost is open
                    if tile_up in open_tiles or can_go_through_gate(tile_up):
                        self.allowed_turns[Direction.UP] = True

                    # If the position below the ghost is open
                    if tile_down in open_tiles or can_go_through_gate(tile_down):
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

                    if tile_left in open_tiles or can_go_through_gate(tile_left):
                        self.allowed_turns[Direction.LEFT] = True

                    if tile_right in open_tiles or can_go_through_gate(tile_right):
                        self.allowed_turns[Direction.RIGHT] = True

            if self.direction in [Direction.LEFT, Direction.RIGHT]:
                if (
                    TILE_CENTER_FACTOR_MIN
                    <= self.rect.centerx % TILE_WIDTH
                    <= TILE_CENTER_FACTOR_MAX
                ):
                    # If the position above the ghost is open
                    if tile_up in open_tiles or can_go_through_gate(tile_up):
                        self.allowed_turns[Direction.UP] = True

                    # If the position below the ghost is open
                    if tile_down in open_tiles or can_go_through_gate(tile_down):
                        self.allowed_turns[Direction.DOWN] = True

                if (
                    TILE_CENTER_FACTOR_MIN
                    <= self.rect.centery % TILE_HEIGHT
                    <= TILE_CENTER_FACTOR_MAX
                ):
                    if tile_left in open_tiles or can_go_through_gate(tile_left):
                        self.allowed_turns[Direction.LEFT] = True

                    if tile_right in open_tiles or can_go_through_gate(tile_right):
                        self.allowed_turns[Direction.RIGHT] = True

    def update_target(self):
        # If a ghost is dead, the goal is to get in the ghost box
        if self.is_dead:
            self.target_position = self.ghost_box["target_position"]
            return

        runaway = Vector2()

        if self.pacman.rect.x < WINDOW_WIDTH / 2:
            runaway.x = WINDOW_WIDTH
        if self.pacman.rect.y < WINDOW_HEIGHT / 2:
            runaway.y = WINDOW_HEIGHT

        # If a power-up is active, the goal is to run away from the Pacman
        if self.timers_manager.power_up_timer.active:
            match self.type:
                case GhostType.BLINKY:
                    self.target_position = runaway
                case GhostType.PINKY:
                    self.target_position = Vector2(self.pacman.rect.x, runaway.y)
                case GhostType.INKY:
                    self.target_position = Vector2(runaway.x, self.pacman.rect.y)
                case GhostType.CLYDE:
                    self.target_position = Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        else:
            # If a ghost is in the box, the goal is to get outside of it
            if self.is_in_box:
                self.target_position = Vector2(400, 100)
            else:
                self.target_position = self.pacman.rect

    def update_speed(self):
        speed_config = self.ghost_config["speed"]

        if self.is_dead:
            self.speed = speed_config["dead"]
        elif self.timers_manager.power_up_timer.active:
            self.speed = speed_config["power_up"]
        else:
            self.speed = speed_config["normal"]

    def detect_collisions(self):
        if not self.is_dead and self.rect.colliderect(self.pacman.rect):
            if self.timers_manager.power_up_timer.active:
                self.is_dead = True
                self.game_state_manager.score += (
                    self.game_state_manager.get_level_config()["score_points"]["ghost"]
                )
                self.asset_manager.sounds[AudioAsset.EAT_GHOST].play()
            else:
                self.game_state_manager.lives -= 1

                if self.game_state_manager.lives >= 0:
                    self.game_state_manager.game_state = GameState.WAITING_TO_START

    def restart(self):
        self.is_dead = False
        self.update_image()

        position = self.ghost_config["position"]
        # Represents a rectangle to figure out where the ghost will be drawn in a current frame
        self.rect = self.image.get_rect(center=position)
        self.direction = self.ghost_config["direction"]

    def move(self):
        # If a ghost is dead or in the box, use the effective way to get
        # in/out the box
        if self.is_dead or self.is_in_box:
            move_towards_target(self)
        else:
            # Else each type uses different movement pattern
            match self.type:
                case GhostType.BLINKY:
                    move_blinky(self)
                case GhostType.PINKY:
                    move_pinky(self)
                case GhostType.INKY:
                    move_inky(self)
                case GhostType.CLYDE:
                    move_towards_target(self)

        if self.rect.centerx > WINDOW_WIDTH + self.rect.width / 4:
            self.rect.centerx = -self.rect.width / 4
        elif self.rect.centerx < -self.rect.width / 4:
            self.rect.centerx = WINDOW_WIDTH + self.rect.width / 4

        top_left = self.ghost_box["top_left"]
        bottom_right = self.ghost_box["bottom_right"]
        if (
            top_left.x < self.rect.x < bottom_right.x
            and top_left.y - 30 < self.rect.y < bottom_right.y
        ):
            self.is_in_box = True

            if self.is_dead and not self.timers_manager.ghost_resurrection_timer.active:
                self.timers_manager.ghost_resurrection_timer.activate(self.resurrect)
        else:
            self.is_in_box = False

    def resurrect(self):
        self.is_dead = False

    def update(self, _delta_time):
        self.update_image()
        self.update_allowed_turns()
        self.update_target()
        self.update_speed()
        self.move()
        self.detect_collisions()
