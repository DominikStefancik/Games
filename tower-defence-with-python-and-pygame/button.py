import pygame


class Button():
    def __init__(self, image, x, y, is_single_click_type) -> None:
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.is_clicked = False
        self.is_single_click_type = is_single_click_type

    def draw(self, surface):
        is_button_clicked = False
        # Get ouse position
        mouse_position = pygame.mouse.get_pos()

        # Check mouseover and clicked event conditions
        #
        # If button's rectangle "collides" with the current mouse position, that means the cursor is over the button
        if self.rect.collidepoint(mouse_position):
            # A user clicked the left mouse button
            if pygame.mouse.get_pressed()[0] == 1 and not self.is_clicked:
                is_button_clicked = True

                if self.is_single_click_type:
                    self.is_clicked = True

            # The left mouse button was clicked and then released
            if pygame.mouse.get_pressed()[0] == 0:
                self.is_clicked = False

        # Draw button on the screen
        surface.blit(self.image, self.rect)

        return is_button_clicked
