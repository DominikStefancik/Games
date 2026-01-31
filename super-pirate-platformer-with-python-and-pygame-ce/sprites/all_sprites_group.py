from settings import pygame, vector, WINDOW_HEIGHT, WINDOW_WIDTH

from .constants import CameraBorder


# We created this class so we can ovewrite the "draw" method and define
# how all sprites should be drawn. This way we can implement a moving camera.
class AllSpritesGroup(pygame.sprite.Group):
    def __init__(self, level_width, level_height, top_limit=0):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = vector()
        self.camera_border = {
            CameraBorder.LEFT: 0,
            # The "level_width" has to be negative, because the further right the player goes,
            # the bigger left offset the camera will have
            # When dealing with the right border we want to mirror the entire camera.
            #
            # When moving the camera, we want the player to be in the middle of the screen.
            # But when he reaches one of the edges, the camera will show the rendered edge of the map
            # and also the black part of the screen which is not covered by the background.
            # We don't want to show it, that's why we have to add the WINDOW_WIDTH
            #
            # The same reasoning is for using negative value of "level_height" and adding WINDOW_HEIGHT
            # for the bottom border below.
            CameraBorder.RIGHT: -level_width + WINDOW_WIDTH,
            CameraBorder.TOP: top_limit,
            CameraBorder.BOTTOM: -level_height + WINDOW_HEIGHT,
        }

    # We want to constraint updating the camera for cases when the player comes close enough to the level map edges.
    # In that case we want the camera to stop moving
    def constraint_camera(self):
        # If the player is close to the left edge, the camera should stay on the left edge
        self.offset.x = (
            self.offset.x
            if self.offset.x < self.camera_border[CameraBorder.LEFT]
            else self.camera_border[CameraBorder.LEFT]
        )
        # If the player is close to the right edge, the camera should stay on the right edge
        self.offset.x = (
            self.offset.x
            if self.offset.x > self.camera_border[CameraBorder.RIGHT]
            else self.camera_border[CameraBorder.RIGHT]
        )
        self.offset.y = (
            self.offset.y
            if self.offset.y < self.camera_border[CameraBorder.TOP]
            else self.camera_border[CameraBorder.TOP]
        )
        self.offset.y = (
            self.offset.y
            if self.offset.y > self.camera_border[CameraBorder.BOTTOM]
            else self.camera_border[CameraBorder.BOTTOM]
        )

    def draw(self):
        # Because this class inherits from "pygame.sprite.Group",
        # the "self" returns all sprites contained in this group
        for sprite in sorted(self, key=lambda sprite: sprite.z_index):
            offset_position = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image, offset_position)

    def update(self, target_position, delta_time):
        # The drawing offset will depend on the position of the target.
        # When the target moves, the camera changes with it.
        # If we set up the player as target, the camera will follow him.
        #
        # We have to set up the negative value, because if the player is moving more right,
        # then we want everyting to move more left. The same for the left side.
        # Note: We want the player to be always in the middle of the screen,
        # that's why we subtrack "WINDOW_WIDTH / 2" and "WINDOW_HEIGHT / 2"
        self.offset.x = -(target_position[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(target_position[1] - WINDOW_HEIGHT / 2)
        self.constraint_camera()

        super().update(delta_time)
