import constants
import pygame

# Initialise PyGame
pygame.init()

# Create a clock to limit the frame rate
clock = pygame.time.Clock()

# Create a game window
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Python Tower Defence")

run = True

# Game loop
while run:
    # 60 frames per second
    clock.tick(constants.FPS)

    # Event handler
    # Events in PyGame are "stored" in an vent queue
    for event in pygame.event.get():
        # Quit program
        if event.type == pygame.QUIT:
            run = False

pygame.quit()
