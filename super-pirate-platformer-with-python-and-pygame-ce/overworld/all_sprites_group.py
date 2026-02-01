from game_state import get_game_state
from settings import pygame, vector, WINDOW_HEIGHT, WINDOW_WIDTH


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

        # Because this class inherits from "pygame.sprite.Group",
        # the "self" returns all sprites contained in this group
        for sprite in sorted(self, key=lambda sprite: sprite.z_index):
            offset_position = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image, offset_position)
