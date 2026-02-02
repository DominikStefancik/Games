from game_state import get_game_state
from settings import ANIMATION_SPEED, pygame, TILE_SIZE, vector, Z_Layer

from .constants import PlayerIconAnimation


class PlayerIcon(pygame.sprite.Sprite):
    def __init__(self, groups, position, animation_frames):
        super().__init__(groups)

        self.animation_frames = animation_frames
        self.frame_index = 0
        self.animation = PlayerIconAnimation.IDLE
        self.image = self.animation_frames[self.animation.value][self.frame_index]
        self.rect = self.image.get_frect(center=position)
        self.z_index = Z_Layer.MAIN.value
        self.current_path = None
        self.direction = vector()
        self.speed = 400

    def start_move(self, path):
        self.rect.center = path[0]
        # We don't need the first position of the path, as it is the position of a node the player icon
        # currently stands on
        self.current_path = path[1:]
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
        if self.current_path:
            self.update_animation()
            self.animate(delta_time)
            self.detect_collision_with_next_path_point()
            self.rect.center += self.direction * self.speed * delta_time
