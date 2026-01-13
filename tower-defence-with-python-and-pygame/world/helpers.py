import pygame

from .constants import MAP_HEIGHT, MAP_WIDTH, SIDE_PANEL_WIDTH

def draw_text(surface, text, font, text_column, x, y):
    # First we have to turn a text into an image
    image = font.render(text, True, text_column)
    surface.blit(image, (x, y))


def display_game_data(surface, world, font, coin_image, heart_image, logo_image):
    # Draw panel
    pygame.draw.rect(surface, "maroon", (MAP_WIDTH, 0, SIDE_PANEL_WIDTH, MAP_HEIGHT))
    pygame.draw.rect(surface, "grey0", (MAP_WIDTH, 0, SIDE_PANEL_WIDTH, 400), 2)
    surface.blit(logo_image, (MAP_WIDTH, 400))

    # Display data
    draw_text(surface, "LEVEL: " + str(world.level), font, "grey100", MAP_WIDTH + 10, 10)
    surface.blit(heart_image, (MAP_WIDTH + 10, 35))
    draw_text(surface, str(world.health), font, "grey100", MAP_WIDTH + 50, 40)
    surface.blit(coin_image, (MAP_WIDTH + 10, 65))
    draw_text(surface, str(world.money), font, "grey100", MAP_WIDTH + 50, 70)
