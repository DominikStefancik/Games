import math

import pygame

from constants import BUTTON_RADIUS, FPS, WINDOW_HEIGHT, WINDOW_WIDTH
from hangman_status import HangmanStatus
from helpers import draw, get_hangman_image_path, show_game_end_message
from game import Game

pygame.init()

# Setup display
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Python Hangman")

# Load images
hangman_images = []
for index in range(7):
    image_path = get_hangman_image_path(index)
    # Every image which gets loaded into a game is turned into a set of pixels called "Surface".
    # Then the Surface can be drawn into the Pygame window.
    image = pygame.image.load(image_path)
    hangman_images.append(image)

# Load fonts
LETTER_FONT = pygame.font.SysFont("comicsans", 25)
WORD_FONT = pygame.font.SysFont("comicsans", 35)
TITLE_FONT = pygame.font.SysFont("comicsans", 45)

game = Game()

# Setup game loop
clock = pygame.time.Clock()
is_running = True

while is_running:
    # Make sure the game loop runs at the speed we set
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position_x, mouse_position_y = pygame.mouse.get_pos()

            # Check if in the time when the click happened the mouse position was "inside" of any of the buttons
            for letter_array in game.letters:
                character, x, y, is_visible = letter_array
                if is_visible:
                    distance = math.sqrt(
                        (x - mouse_position_x) ** 2 + (y - mouse_position_y) ** 2
                    )

                    if distance < BUTTON_RADIUS:
                        game.guessed_letters.append(character)
                        # After we clicked on a button, we will make it invisible,
                        # so the player cannot click on it multiple times
                        letter_array[3] = False

                        if character not in game.word:
                            game.update_status()

    draw(
        WINDOW,
        TITLE_FONT,
        game,
        hangman_images,
        LETTER_FONT,
        WORD_FONT,
    )

    game_won = True
    for letter in game.word:
        if letter not in game.guessed_letters:
            game_won = False
            break

    if game_won:
        show_game_end_message(WINDOW, WORD_FONT, "You WON!")
        game.reset()

    if game.hangman_status == HangmanStatus.BOTH_LEGS:
        show_game_end_message(WINDOW, WORD_FONT, "You LOST!")
        game.reset()


pygame.quit()
