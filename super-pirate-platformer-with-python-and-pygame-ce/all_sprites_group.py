from settings import pygame, vector, WINDOW_HEIGHT, WINDOW_WIDTH


# We created this class so we can ovewrite the "draw" method and define
# how all sprites should be drawn. This way we can implement a moving camera.
class AllSpritesGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = vector()

    def draw(self, target_position):
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

        # Because this class inherits from "pygame.sprite.Group",
        # the "self" return all sprites contained in this group
        for sprite in self:
            offset_position = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image, offset_position)
