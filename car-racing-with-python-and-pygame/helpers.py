import pygame

def scale_image(image, scale_factor):
    new_size = round(image.get_width() * scale_factor), round(image.get_height() * scale_factor)

    return pygame.transform.scale(image, new_size)


def draw(surface, images, player_car):
    for image, position in images:
        # PyGame coordinates for displaying images start at left top corner
        surface.blit(image, position)

    player_car.draw(surface)

    # Update display
    # Takes all of the changes from a "queue" and displays them
    pygame.display.update()
