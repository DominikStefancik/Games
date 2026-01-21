import math

import pygame

from constants import BUTTON_GAP_SIZE, BUTTONS_IN_ROW, BUTTON_RADIUS, BUTTON_ROWS, FPS, LETTER_A_ASCII_CODE, WINDOW_HEIGHT, WINDOW_WIDTH
from hangman_status import HangmanStatus
from helpers import draw, get_hangman_image_path

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
LETTER_FONT = pygame.font.SysFont('comicsans', 25)

# Game variables
hangman_status = HangmanStatus.EMPTY_ROPE

# Each letter will be an array of items [character, x-position, y-position, is_visible]
# We want to modify properties of these items and with using an array it is easier than using a tuple
# (see setting up visibility after a player clicks on a letter)
letters = []
distance_between_two_buttons = BUTTON_RADIUS * 2 + BUTTON_GAP_SIZE
button_start_position_x = round((WINDOW_WIDTH - distance_between_two_buttons * BUTTONS_IN_ROW) / BUTTON_ROWS)
button_start_position_y = 430
for index in range(26):
    position_x = button_start_position_x + BUTTON_GAP_SIZE * 2 + distance_between_two_buttons * (index % BUTTONS_IN_ROW)
    position_y = button_start_position_y + (index // BUTTONS_IN_ROW) * distance_between_two_buttons
    # The function "chr()" returns a character representation of the number we give it as a parameter
    letters.append([chr(LETTER_A_ASCII_CODE + index), position_x, position_y, True])

# Setup game loop
clock = pygame.time.Clock()
is_running = True

while is_running:
    # Make sure the game loop runs at the speed we set
    clock.tick(FPS)

    draw(WINDOW, hangman_images, hangman_status, letters, LETTER_FONT)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           is_running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position_x, mouse_position_y = pygame.mouse.get_pos()

            # Check if in the time when the click happned the mouse position was "inside" of any of the buttons
            for letter_array in letters:
                character, x, y, is_visible = letter_array
                if is_visible:
                    distance = math.sqrt((x - mouse_position_x) ** 2 + (y - mouse_position_y) ** 2)

                    if distance < BUTTON_RADIUS:
                        # After we clicked on a button, we will make it invisible,
                        # so the player cannot click on it multiple times
                        letter_array[3] = False



pygame.quit()
