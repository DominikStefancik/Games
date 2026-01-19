import random

import pygame

from constants import BACKGROUND_IMAGE_HEIGHT, BACKGROUND_IMAGE_PATH, FPS, WHITE, WINDOW_HEIGHT, WINDOW_WIDTH
from helpers import draw_background, draw_text
from jumping_platform.constants import MAX_PLATFORMS_COUNT, PLATFORM_IMAGE_PATH
from jumping_platform.helpers import create_starting_platform
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
game_score = 0
is_game_over = False

# Create a game window
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Python Jumpy")

# Load images
background_image = pygame.image.load(BACKGROUND_IMAGE_PATH).convert_alpha()
jumpy_image = pygame.image.load(JUMPY_IMAGE_PATH).convert_alpha()
platform_image = pygame.image.load(PLATFORM_IMAGE_PATH).convert_alpha()

# Define fonts
SMALL_FONT = pygame.font.SysFont("Lucida Sans", 20)
BIG_FONT = pygame.font.SysFont("Lucida Sans", 24)

# The operator "//" ensures that a number division returns always an integer
JUMPY_INITIAL_POSITION = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 150)
jumpy = Player(jumpy_image, JUMPY_INITIAL_POSITION)

# Create Sprite groups
platform_group = pygame.sprite.Group()

# Create starting platform
platform = create_starting_platform(platform_image)
platform_group.add(platform)

is_running = True
# Game loop
while is_running:
    # 60 frames per second
    clock.tick(FPS)

    if not is_game_over:
        # The "background_scroll" will keep increasing, whereas the "window_scroll" will keep reseting to 0
        background_scroll += window_scroll

        # This ensures that the position of the second image we added in the "draw_background" function
        # will be reset after it has been scrolled down.
        # With this we achieve an infinite background scrolling.
        if background_scroll >= BACKGROUND_IMAGE_HEIGHT:
            background_scroll = 0

        draw_background(WINDOW, background_image, background_scroll)

        # Generate platforms
        if len(platform_group) < MAX_PLATFORMS_COUNT:
            platform_width = random.randint(40, 60)
            platform_x = random.randint(0, WINDOW_WIDTH - platform_width)
            # Take the Y-coordinate of the previously created platform
            # and set the Y-coordinate of the next platform depending on the previous one
            platform_y = platform.rect.y - random.randint(80, 120)
            platform = Platform(platform_image, (platform_x, platform_y), platform_width)
            platform_group.add(platform)

        platform_group.update(window_scroll)

        # Draw sprites
        platform_group.draw(WINDOW)
        jumpy.draw(WINDOW)

        window_scroll = jumpy.move(platform_group)

        # Check if the game is over
        if jumpy.rectangle.top > WINDOW_HEIGHT:
            is_game_over = True
    else: # The game is over
        draw_text(WINDOW, BIG_FONT, "GAME OVER!", WHITE, (130, 200))
        draw_text(WINDOW, BIG_FONT, f"SCORE: {str(game_score)}", WHITE, (130, 250))
        draw_text(WINDOW, BIG_FONT, "PRESS SPACE TO PLAY AGAIN", WHITE, (60, 300))

        # Process key presses
        key = pygame.key.get_pressed()

        if key[pygame.K_SPACE]:
            # Reset game variables
            is_game_over = False
            game_score = 0
            window_scroll = 0

            # Reposition jumpy
            jumpy.rectangle.center = JUMPY_INITIAL_POSITION

            # Reset platforms
            platform_group.empty()
            platform = create_starting_platform(platform_image)
            platform_group.add(platform)



    # Event handler
    # Events in Pygame are "stored" in an event queue
    for event in pygame.event.get():
        # Quit program
        if event.type == pygame.QUIT:
            is_running = False

    # By updating display window we tell Pygame to execute all displaying methods, like "blit()"
    pygame.display.update()

pygame.quit()
