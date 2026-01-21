import pygame

from constants import FPS, WHITE, WINDOW_HEIGHT, WINDOW_WIDTH
from hangman_status import HangmanStatus
from helpers import get_hangman_image_path

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

# Game variables
hangman_status = HangmanStatus.EMPTY_ROPE

# Setup game loop
clock = pygame.time.Clock()
is_running = True

while is_running:
    # Make sure the game loop runs at the speed we set
    clock.tick(FPS)

    # Fill the background of the game window
    WINDOW.fill(WHITE)
    WINDOW.blit(hangman_images[int(hangman_status)], (150, 100))
    # In Pygame we have to manually say when we want to display on the screen everything we drew so far
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           is_running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            print(mouse_position)


pygame.quit()
