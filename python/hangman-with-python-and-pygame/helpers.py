from os.path import join

import pygame

from constants import (
    BLACK,
    BUTTON_CIRCLE_THICKNESS,
    BUTTON_RADIUS,
    WHITE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    WORDS,
)


def get_hangman_image_path(index):
    return join("assets", "images", f"hangman_{index}.png")


def draw(
    surface,
    title_font,
    game,
    hangman_images,
    letter_font,
    word_font,
):
    # Fill the background of the game window
    surface.fill(WHITE)
    surface.blit(hangman_images[int(game.hangman_status)], (150, 100))

    # Draw title
    text = title_font.render("HANGMAN", 1, BLACK)
    surface.blit(text, (WINDOW_WIDTH / 2 - text.get_width() / 2, 20))

    # Draw word
    display_word = ""
    for letter in game.word:
        if letter in game.guessed_letters:
            display_word += letter + " "
        else:
            display_word += "_ "

    text = word_font.render(display_word, 1, BLACK)
    surface.blit(text, (400, 200))

    # Draw letters
    for letter_array in game.letters:
        character, x, y, is_visible = letter_array
        # If a letter is invisible, that means a player already clicked on it.
        # In that case we don't want to show it, so the player will not be able to click on it multiple times.
        if is_visible:
            pygame.draw.circle(
                surface, BLACK, (x, y), BUTTON_RADIUS, BUTTON_CIRCLE_THICKNESS
            )
            text = letter_font.render(character, 1, BLACK)
            surface.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

    # In Pygame we have to manually say when we want to display on the screen everything we drew so far
    pygame.display.update()


def show_game_end_message(surface, font, message):
    pygame.time.delay(1000)
    surface.fill(WHITE)
    text = font.render(message, 1, BLACK)
    surface.blit(
        text,
        (
            WINDOW_WIDTH / 2 - text.get_width() / 2,
            WINDOW_HEIGHT / 2 - text.get_height() / 2,
        ),
    )
    pygame.display.update()
    pygame.time.delay(2000)
