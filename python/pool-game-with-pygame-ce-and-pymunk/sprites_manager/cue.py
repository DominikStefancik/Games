import pygame


class Cue:
    def __init__(self, image, position) -> None:
        self.angle = 0
        # When rotating and image, we have to preserve the original image,
        # otherwise the used image will lose quality everytime we rotate it
        self.original_image = image
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_frect(center=position)

    def update(self, position, angle):
        self.rect.center = position
        self.angle = angle

    def draw(self, surface):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        surface.blit(
            self.image,
            (
                self.rect.centerx - self.image.get_width() / 2,
                self.rect.centery - self.image.get_height() / 2,
            ),
        )
