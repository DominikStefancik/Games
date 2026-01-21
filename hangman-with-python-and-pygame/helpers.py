import pygame

from constants import BLACK, BUTTON_CIRCLE_THICKNESS, BUTTON_RADIUS, WHITE

def get_hangman_image_path(index):
    return f"assets/images/hangman_{index}.png"


def draw(surface, hangman_images, hangman_status, letters, font):
    # Fill the background of the game window
    surface.fill(WHITE)
    surface.blit(hangman_images[int(hangman_status)], (150, 100))

    # Draw letters
    for letter_array in letters:
        character, x, y, is_visible = letter_array
        # If a letter is invisible, that means a player already clicked on it.
        # In that case we don't want to show it, so the player will not be able to click on it multiple times.
        if is_visible:
            pygame.draw.circle(surface, BLACK, (x, y), BUTTON_RADIUS, BUTTON_CIRCLE_THICKNESS)
            text = font.render(character, 1, BLACK)
            surface.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

    # In Pygame we have to manually say when we want to display on the screen everything we drew so far
    pygame.display.update()
