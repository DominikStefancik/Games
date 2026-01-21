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

# Letters variables
letters = []
distance_between_two_buttons = BUTTON_RADIUS * 2 + BUTTON_GAP_SIZE
button_start_position_x = round((WINDOW_WIDTH - distance_between_two_buttons * BUTTONS_IN_ROW) / BUTTON_ROWS)
button_start_position_y = 430
for index in range(26):
    position_x = button_start_position_x + BUTTON_GAP_SIZE * 2 + distance_between_two_buttons * (index % BUTTONS_IN_ROW)
    position_y = button_start_position_y + (index // BUTTONS_IN_ROW) * distance_between_two_buttons
    # The function "chr()" returns a character representation of the number we give it as a parameter
    letters.append((chr(LETTER_A_ASCII_CODE + index), position_x, position_y))

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
            mouse_position = pygame.mouse.get_pos()
            print(mouse_position)


pygame.quit()
