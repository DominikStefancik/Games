import pygame

def scale_image(image, scale_factor):
    new_size = round(image.get_width() * scale_factor), round(image.get_height() * scale_factor)

    return pygame.transform.scale(image, new_size)


def draw(surface, images, computer_car, player_car, game_info, font, window_height):
    for image, position in images:
        # PyGame coordinates for displaying images start at left top corner
        surface.blit(image, position)

    level_text = font.render(f"Level {game_info.level}", 1, (255, 255, 255))
    surface.blit(level_text, (10, window_height - level_text.get_height() - 70))

    time_text = font.render(f"Time: {game_info.get_level_time()}s", 1, (255, 255, 255))
    surface.blit(time_text, (10, window_height - time_text.get_height() - 40))

    player_car_velocity_text = font.render(f"Velocity: {round(player_car.velocity, 1)}px/s", 1, (255, 255, 255))
    surface.blit(player_car_velocity_text, (10, window_height - player_car_velocity_text.get_height() - 10))

    computer_car.draw(surface)
    player_car.draw(surface)

    # Update display
    # Takes all of the changes from a "queue" and displays them
    pygame.display.update()


def render_text_center(surface, font, text):
    # The second argument defines anti-aliasing
    text_render = font.render(text, 1, (10, 10, 10))
    surface.blit(text_render, (surface.get_width() / 2 - text_render.get_width() / 2, surface.get_height() / 2 - text_render.get_height() / 2 - 25))
