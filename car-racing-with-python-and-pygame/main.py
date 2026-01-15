import pygame
import time
import math

from car.player_car import PlayerCar
from constants import CAR_IMAGE_SCALE, FINISH_LINE_PATH, FPS, GRASS_PATH, GREEN_CAR_PATH, RED_CAR_PATH, TRACK_IMAGE_SCALE, TRACK_PATH, TRACK_BORDER_PATH
from helpers import draw, scale_image

# Load images
GRASS_IMAGE = scale_image(pygame.image.load(GRASS_PATH), 2.5)
TRACK_IMAGE = scale_image(pygame.image.load(TRACK_PATH), TRACK_IMAGE_SCALE)
TRACK_BORDER_IMAGE = scale_image(pygame.image.load(TRACK_BORDER_PATH), TRACK_IMAGE_SCALE)
FINISH_LINE_IMAGE = pygame.image.load(FINISH_LINE_PATH)
GREEN_CAR_IMAGE = scale_image(pygame.image.load(GREEN_CAR_PATH), 1)
RED_CAR_IMAGE = scale_image(pygame.image.load(RED_CAR_PATH), CAR_IMAGE_SCALE)

# Set up window
WINDOW_WIDTH, WINDOW_HEIGHT = TRACK_IMAGE.get_width(), TRACK_IMAGE.get_height()
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Python Car Racing")

clock = pygame.time.Clock()

images_to_draw = [(GRASS_IMAGE, (0, 0)), (TRACK_IMAGE, (0, 0))]
player_car = PlayerCar(RED_CAR_IMAGE, (180, 200), 4, 4)

is_running = True
while is_running:
    # Set up a clock to make sure that the game loop is not going to run faster than certain speed (frame per second)
    # Otherwise the loop will run as fast as the computer processor allows
    # Wit setting up the clock we ensure that our game speed is the same on different computers
    # with slow or fast processors
    clock.tick(FPS)

    draw(WINDOW, images_to_draw, player_car)

    for event in pygame.event.get():
        # Quit program
        if event.type == pygame.QUIT:
            is_running = False
            break

pygame.quit()
