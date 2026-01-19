import random

import pygame

from constants import BACKGROUND_IMAGE_HEIGHT, BACKGROUND_IMAGE_PATH, FPS, VERTICAL_SCROLL_THRESSHOLD, WHITE, WINDOW_HEIGHT, WINDOW_WIDTH
from helpers import draw_background
from jumping_platform.constants import MAX_PLATFORMS_COUNT, PLATFORM_IMAGE_PATH
from jumping_platform.platform import Platform
from player.constants import JUMPY_IMAGE_PATH
from player.player import Player

# Initialise Pygame
pygame.init()

# Create a clock to limit the frame rate
clock = pygame.time.Clock()

# Game variables
window_scroll = 0
background_scroll = 0

# Create a game window
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Python Jumpy")

# Load images
background_image = pygame.image.load(BACKGROUND_IMAGE_PATH).convert_alpha()
jumpy_image = pygame.image.load(JUMPY_IMAGE_PATH).convert_alpha()
platform_image = pygame.image.load(PLATFORM_IMAGE_PATH).convert_alpha()

# The operator "//" ensures that a number division returns always an integer
jumpy = Player(jumpy_image, (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 150))

# Create Sprite groups
platform_group = pygame.sprite.Group()

# Create temporary platforms
for index in range(MAX_PLATFORMS_COUNT):
    width = random.randint(40, 60)
    x = random.randint(0, WINDOW_WIDTH - width)
    y = index * random.randint(80, 120)
    platform = Platform(platform_image, (x, y), width)
    platform_group.add(platform)

is_running = True
# Game loop
while is_running:
    # 60 frames per second
    clock.tick(FPS)

    # The "background_scroll" will keep increasing, whereas the "window_scroll" will keep reseting to 0
    background_scroll += window_scroll

    # This ensures that the position of the second image we added in the "draw_background" function
    # will be reset after it has been scrolled down.
    # With this we achieve an infinite background scrolling.
    if background_scroll >= BACKGROUND_IMAGE_HEIGHT:
        background_scroll = 0

    draw_background(WINDOW, background_image, background_scroll)

    # Draw temporary scroll threshold
    pygame.draw.line(WINDOW, WHITE, (0, VERTICAL_SCROLL_THRESSHOLD), (WINDOW_WIDTH, VERTICAL_SCROLL_THRESSHOLD))

    platform_group.update(window_scroll)

    # Draw sprites
    platform_group.draw(WINDOW)
    jumpy.draw(WINDOW)

    window_scroll = jumpy.move(platform_group)

    # Event handler
    # Events in Pygame are "stored" in an event queue
    for event in pygame.event.get():
        # Quit program
        if event.type == pygame.QUIT:
            is_running = False

    # By updating diplay window we tell Pygame to execute all displaying methods, like "blit()"
    pygame.display.update()

pygame.quit()
