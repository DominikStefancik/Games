import pygame

from constants import BACKGROUND_IMAGE_PATH, WINDOW_HEIGHT, WINDOW_WIDTH

# Initialise Pygame
pygame.init()

# Create a game window
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Python Jumpy")

# Load images
background_image = pygame.image.load(BACKGROUND_IMAGE_PATH).convert_alpha()

is_running = True
# Game loop
while is_running:
    # Draw background
    # The second argument is a tuple with coordinates where the top left corner of the image
    # will be placed.
    WINDOW.blit(background_image, (0, 0))


    # Event handler
    # Events in Pygame are "stored" in an event queue
    for event in pygame.event.get():
        # Quit program
        if event.type == pygame.QUIT:
            is_running = False

    # By updating diplay window we tell Pygame to execute all displaying methods, like "blit()"
    pygame.display.update()

pygame.quit()
