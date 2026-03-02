from game_state.game_state import get_game_state
from settings import pygame, vector, WINDOW_HEIGHT, WINDOW_WIDTH, Z_Layer


# We created this class so we can ovewrite the "draw" method and define
# how all sprites should be drawn. This way we can implement a moving camera.
class AllSpritesGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.game_state = get_game_state()
        self.offset = vector()

    def draw(self, target_position):
        self.offset.x = -(target_position[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(target_position[1] - WINDOW_HEIGHT / 2)

        # Draw the background first
        #
        # Because this class inherits from "pygame.sprite.Group",
        # the "self" returns all sprites contained in this group
        for sprite in sorted(self, key=lambda sprite: sprite.z_index):
            if sprite.z_index < Z_Layer.MAIN.value:
                offset_position = sprite.rect.topleft + self.offset

                if sprite.z_index == Z_Layer.PATH.value:
                    if sprite.level <= self.game_state.unlocked_level:
                        self.display_surface.blit(sprite.image, offset_position)

                else:
                    self.display_surface.blit(sprite.image, offset_position)

        # Then draw the main layer
        #
        # We want to sort the sprites depending on their Y-coordinate and where on the map they are located.
        # The lower they are located, later they are drawn.
        # With this we will handle of drawing the case when the player icon is drawn behind a palm
        # and not to of it.
        for sprite in sorted(self, key=lambda sprite: sprite.rect.centery):
            if sprite.z_index == Z_Layer.MAIN.value:
                offset_position = sprite.rect.topleft + self.offset
                self.display_surface.blit(sprite.image, offset_position)
