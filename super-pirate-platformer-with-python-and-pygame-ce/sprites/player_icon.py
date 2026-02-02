from game_state.constants import GameStage
from game_state.game_state import get_game_state
from overworld.constants import OverworldPathProperty
from settings import ANIMATION_SPEED, pygame, TILE_SIZE, vector, Z_Layer

from .constants import NodePathDirection, PlayerIconAnimation


class PlayerIcon(pygame.sprite.Sprite):
    def __init__(self, groups, position, animation_frames, node_sprites, paths):
        super().__init__(groups)

        self.animation_frames = animation_frames
        self.frame_index = 0
        self.animation = PlayerIconAnimation.IDLE
        self.image = self.animation_frames[self.animation.value][self.frame_index]
        self.rect = self.image.get_frect(center=position)
        self.z_index = Z_Layer.MAIN.value
        self.node_sprites = node_sprites
        self.current_node = None
        self.paths = paths
        self.current_path = None
        self.direction = vector()
        self.speed = 400

    def process_key_input(self):
        keys = pygame.key.get_pressed()

        # Allow reaction to key strokes only if the player icon is standing on a node
        if self.current_node and not self.current_path:
            if keys[pygame.K_LEFT] and self.current_node.has_path_in_direction(
                NodePathDirection.LEFT.value
            ):
                self.move(NodePathDirection.LEFT.value)
            if keys[pygame.K_RIGHT] and self.current_node.has_path_in_direction(
                NodePathDirection.RIGHT.value
            ):
                self.move(NodePathDirection.RIGHT.value)
            if keys[pygame.K_UP] and self.current_node.has_path_in_direction(
                NodePathDirection.UP.value
            ):
                self.move(NodePathDirection.UP.value)
            if keys[pygame.K_DOWN] and self.current_node.has_path_in_direction(
                NodePathDirection.DOWN.value
            ):
                self.move(NodePathDirection.DOWN.value)
            if keys[pygame.K_RETURN]:
                game_state = get_game_state()
                game_state.current_level = self.current_node.level
                game_state.switch_stage(GameStage.LEVEL)

    def move(self, direction):
        # In Tiled, the value can contain letter "r" which means reverse.
        # That means this particular paths leaads to a node of a previous level.
        # That also means we have to extract the number from a string.
        path_key = int(self.current_node.available_paths[direction][0])
        is_reverse_path = self.current_node.available_paths[direction][-1] == "r"
        # Get all position points from a path if it is not reverse
        # If it is reverse, get the points in a reverse order
        path_points = (
            self.paths[path_key][OverworldPathProperty.POSITION_POINT][:]
            if not is_reverse_path
            else self.paths[path_key][OverworldPathProperty.POSITION_POINT][::-1]
        )

        # Start moving
        self.rect.center = path_points[0]
        # We don't need the first position of the path, as it is the position of a node the player icon
        # currently stands on
        self.current_path = path_points[1:]
        self.find_path_direction()

    def find_path_direction(self):
        if self.current_path:
            # Compare player icon's coordinates to the coordinates of the next point of the path
            if (
                self.rect.centerx == self.current_path[0][0]
            ):  # the player icon can move on the vertical axis
                self.direction = vector(
                    0, 1 if self.current_path[0][1] > self.rect.centery else -1
                )
            else:  # the player icon can move on the vertical axis
                self.direction = vector(
                    1 if self.current_path[0][0] > self.rect.centerx else -1, 0
                )
        else:
            self.direction = vector()

    def detect_collision_with_next_path_point(self):
        reached_node_going_left = (
            self.direction.x == -1 and self.rect.centerx <= self.current_path[0][0]
        )
        reached_node_going_right = (
            self.direction.x == 1 and self.rect.centerx >= self.current_path[0][0]
        )
        if reached_node_going_left or reached_node_going_right:
            # After the player icon reached the next point, set it as its position and then delete it from the path
            # because after that we want to find the next point he should be moving to
            self.rect.centerx = self.current_path[0][0]
            del self.current_path[0]
            # After we delete the point from the path, the condition "self.current_path" in the "find_path_direction"
            # will be False which will cause the player to stop moving
            self.find_path_direction()

        reached_node_going_up = (
            self.direction.y == -1 and self.rect.centery <= self.current_path[0][1]
        )
        reached_node_going_down = (
            self.direction.y == 1 and self.rect.centery >= self.current_path[0][1]
        )
        if reached_node_going_up or reached_node_going_down:
            # After the player icon reached the next point, set it as its position and then delete it from the path
            # because after that we want to find the next point he should be moving to
            self.rect.centery = self.current_path[0][1]
            del self.current_path[0]
            self.find_path_direction()

    def update_current_node(self):
        nodes = pygame.sprite.spritecollide(self, self.node_sprites, False)

        if nodes:
            self.current_node = nodes[0]

    def update_animation(self):
        self.animation = PlayerIconAnimation.IDLE

        if self.direction.x == -1:
            self.animation = PlayerIconAnimation.LEFT
        if self.direction.x == 1:
            self.animation = PlayerIconAnimation.RIGHT
        if self.direction.y == -1:
            self.animation = PlayerIconAnimation.UP
        if self.direction.y == 1:
            self.animation = PlayerIconAnimation.DOWN

    def animate(self, delta_time):
        animation_frames = self.animation_frames[self.animation.value]
        self.frame_index += ANIMATION_SPEED * delta_time
        self.image = animation_frames[int(self.frame_index % len(animation_frames))]

    def update(self, delta_time):
        self.process_key_input()
        self.update_current_node()

        if self.current_path:
            self.detect_collision_with_next_path_point()
            self.rect.center += self.direction * self.speed * delta_time

        self.update_animation()
        self.animate(delta_time)
