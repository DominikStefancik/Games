import os

import pygame

from constants import (
    BACKGROUND_IMAGE_HEIGHT,
    BACKGROUND_IMAGE_PATH,
    FPS,
    VERTICAL_SCROLL_THRESHOLD,
    WHITE,
    WINDOW_FADE_COUNTER_TRANSITION,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from bird.constants import BIRD_IMAGE_PATH, MAX_BIRDS_COUNT
from bird.helpers import create_bird
from helpers import draw_background, draw_fading_rectangles, draw_score_panel, draw_text
from jumping_platform.constants import MAX_PLATFORMS_COUNT, PLATFORM_IMAGE_PATH
from jumping_platform.helpers import create_starting_platform, create_platform
from jumping_platform.platform import Platform
from player.constants import JUMPY_IMAGE_PATH
from player.player import Player
from spritesheet import SpriteSheet

# Initialise Pygame
pygame.init()

# Create a clock to limit the frame rate
clock = pygame.time.Clock()

# Game variables
window_scroll = 0
background_scroll = 0
current_score = 0
is_game_over = False
window_fade_counter = 0

if os.path.exists("best_score.txt"):
    # Open the file for reading
    with open("best_score.txt", "r") as file:
        best_score = int(file.read())
else:
    best_score = 0

# Create a game window
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Python Jumpy")

# Load images
background_image = pygame.image.load(BACKGROUND_IMAGE_PATH).convert_alpha()
jumpy_image = pygame.image.load(JUMPY_IMAGE_PATH).convert_alpha()
platform_image = pygame.image.load(PLATFORM_IMAGE_PATH).convert_alpha()
bird_image = pygame.image.load(BIRD_IMAGE_PATH).convert_alpha()
bird_sprite_sheet = SpriteSheet(bird_image)

# Define fonts
SMALL_FONT = pygame.font.SysFont("Lucida Sans", 20)
BIG_FONT = pygame.font.SysFont("Lucida Sans", 24)

# The operator "//" ensures that a number division returns always an integer
JUMPY_INITIAL_POSITION = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 150)
jumpy = Player(jumpy_image, JUMPY_INITIAL_POSITION)

# Create Sprite groups
platform_group = pygame.sprite.Group()
bird_group = pygame.sprite.Group()

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

        # Create platforms
        if len(platform_group) < MAX_PLATFORMS_COUNT:
            platform = create_platform(platform_image, platform, current_score)
            platform_group.add(platform)

        platform_group.update(window_scroll)

        # Create birds
        if len(bird_group) < MAX_BIRDS_COUNT:
            bird = create_bird(bird_sprite_sheet, current_score)

            if bird:
                bird_group.add(bird)

        bird_group.update(window_scroll)

        # Whenever the player hits the threshold and we need to scroll the window, update score
        if window_scroll > 0:
            current_score += window_scroll

        # Draw a line where the previous best score was
        pygame.draw.line(
            WINDOW,
            WHITE,
            (0, current_score - best_score + VERTICAL_SCROLL_THRESHOLD),
            (WINDOW_WIDTH, current_score - best_score + VERTICAL_SCROLL_THRESHOLD),
            3,
        )
        draw_text(
            WINDOW,
            SMALL_FONT,
            f"BEST SCORE: {best_score}",
            WHITE,
            (
                5,
                current_score - best_score + VERTICAL_SCROLL_THRESHOLD + 5,
            ),
        )

        # Draw sprites
        platform_group.draw(WINDOW)
        bird_group.draw(WINDOW)
        jumpy.draw(WINDOW)

        window_scroll = jumpy.move(platform_group)

        draw_score_panel(WINDOW, SMALL_FONT, current_score)

        # Check if the game is over
        if jumpy.rectangle.top > WINDOW_HEIGHT:
            is_game_over = True
    else:  # The game is over
        if window_fade_counter < WINDOW_WIDTH:
            window_fade_counter += WINDOW_FADE_COUNTER_TRANSITION
            draw_fading_rectangles(WINDOW, window_fade_counter)
        else:  # after the fade effect is complete, show text
            draw_text(WINDOW, BIG_FONT, "GAME OVER!", WHITE, (130, 200))
            draw_text(
                WINDOW, BIG_FONT, f"SCORE: {str(current_score)}", WHITE, (130, 250)
            )
            draw_text(WINDOW, BIG_FONT, "PRESS SPACE TO PLAY AGAIN", WHITE, (60, 300))

            if current_score > best_score:
                best_score = current_score
                # Open the file for writting
                with open("best_score.txt", "w") as file:
                    file.write(str(best_score))

            # Process key presses
            key = pygame.key.get_pressed()

            if key[pygame.K_SPACE]:
                # Reset game variables
                is_game_over = False
                current_score = 0
                window_scroll = 0
                window_fade_counter = 0

                # Reposition jumpy
                jumpy.rectangle.center = JUMPY_INITIAL_POSITION

                # Reset platforms
                platform_group.empty()
                platform = create_starting_platform(platform_image)
                platform_group.add(platform)

                # Reset birds
                bird_group.empty()

    # Event handler
    # Events in Pygame are "stored" in an event queue
    for event in pygame.event.get():
        # Quit program
        if event.type == pygame.QUIT:
            is_running = False

    # By updating display window we tell Pygame to execute all displaying methods, like "blit()"
    pygame.display.update()

pygame.quit()
