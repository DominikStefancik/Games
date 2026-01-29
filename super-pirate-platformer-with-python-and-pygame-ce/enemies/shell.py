from settings import ANIMATION_SPEED, pygame, vector, Z_Layer
from timer import Timer

from .constants import ShellAnimation


class Shell(pygame.sprite.Sprite):
    def __init__(
        self, groups, position, animation_frames, reverse, player, create_pearl_function
    ):
        super().__init__(groups)

        if reverse:
            self.animation_frames = {}
            for key, surfaces in animation_frames.items():
                self.animation_frames[key] = [
                    pygame.transform.flip(surface, True, False) for surface in surfaces
                ]

            self.bullet_direction = -1
        else:
            self.animation_frames = animation_frames
            self.bullet_direction = 1

        self.frame_index = 0
        self.animation = ShellAnimation.IDLE
        self.image = self.animation_frames[self.animation.value][self.frame_index]
        self.rect = self.image.get_frect(topleft=position)
        self.previous_rect = self.rect.copy()
        self.z_index = Z_Layer.MAIN.value
        self.player = player
        self.shooting_distance = 500
        self.vertical_level_proximity = 30
        self.shoot_timer = Timer(3000)
        self.has_fired = False
        self.create_pearl = create_pearl_function

    def update_animation(self):
        player_position, shell_position = vector(self.player.rect.center), vector(
            self.rect.center
        )
        is_player_near_enough = (
            shell_position.distance_to(player_position) < self.shooting_distance
        )
        is_player_in_front = (
            shell_position.x < player_position.x
            if self.bullet_direction == 1
            else shell_position.x > player_position.x
        )
        is_player_on_same_level = (
            abs(shell_position.y - player_position.y) < self.vertical_level_proximity
        )

        if (
            is_player_near_enough
            and is_player_in_front
            and is_player_on_same_level
            and not self.shoot_timer.active
        ):
            self.animation = ShellAnimation.FIRE
            self.frame_index = 0
            self.shoot_timer.activate()

    def animate(self, delta_time):
        animation_frames = self.animation_frames[self.animation.value]
        self.frame_index += ANIMATION_SPEED * delta_time

        if self.frame_index < len(animation_frames):
            self.image = animation_frames[int(self.frame_index)]

            if (
                self.animation == ShellAnimation.FIRE
                and int(self.frame_index) == 3
                and not self.has_fired
            ):
                self.create_pearl(self.rect.center, self.bullet_direction)
                self.has_fired = True
        else:
            self.frame_index = 0

            if self.animation == ShellAnimation.FIRE:
                self.animation = ShellAnimation.IDLE
                self.has_fired = False

    def update(self, delta_time):
        self.shoot_timer.update()
        self.update_animation()
        self.animate(delta_time)
