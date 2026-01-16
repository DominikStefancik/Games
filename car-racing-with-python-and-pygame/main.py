import pygame
import time

from car.computer_car import ComputerCar
from car.player_car import PlayerCar
from car.helpers import handle_cars_collision, move_player_car
from car.constants import CAR_IMAGE_SCALE, COMPUTER_CAR_PATH, GREEN_CAR_PATH, RED_CAR_PATH
from constants import FINISH_LINE_PATH, FINISH_LINE_POSITION, FPS, GRASS_PATH, TRACK_IMAGE_SCALE, TRACK_PATH, TRACK_BORDER_PATH
from helpers import draw, scale_image

# Load images
GRASS_IMAGE = scale_image(pygame.image.load(GRASS_PATH), 2.5)
TRACK_IMAGE = scale_image(pygame.image.load(TRACK_PATH), TRACK_IMAGE_SCALE)
TRACK_BORDER_IMAGE = scale_image(pygame.image.load(TRACK_BORDER_PATH), TRACK_IMAGE_SCALE)
FINISH_LINE_IMAGE = pygame.image.load(FINISH_LINE_PATH)
GREEN_CAR_IMAGE = scale_image(pygame.image.load(GREEN_CAR_PATH), CAR_IMAGE_SCALE)
RED_CAR_IMAGE = scale_image(pygame.image.load(RED_CAR_PATH), CAR_IMAGE_SCALE)

# Create masks which will be used for the pixel perfect collision detection
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER_IMAGE)
FINISH_LINE_MASK = pygame.mask.from_surface(FINISH_LINE_IMAGE)

# Set up window
WINDOW_WIDTH, WINDOW_HEIGHT = TRACK_IMAGE.get_width(), TRACK_IMAGE.get_height()
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Python Car Racing")

clock = pygame.time.Clock()

# We are using the track border image to overlap the finish line image
# so it looks that the finish line doesn't go over the track border.
images_to_draw = [(GRASS_IMAGE, (0, 0)), (TRACK_IMAGE, (0, 0)), (FINISH_LINE_IMAGE, FINISH_LINE_POSITION), (TRACK_BORDER_IMAGE, (0, 0))]
player_car = PlayerCar(RED_CAR_IMAGE, (180, 200), 4, 4)
computer_car = ComputerCar(GREEN_CAR_IMAGE, (150, 200), 4, 4, COMPUTER_CAR_PATH)

is_running = True
while is_running:
    # Set up a clock to make sure that the game loop is not going to run faster than certain speed (frame per second).
    # Otherwise the loop will run as fast as the computer processor allows.
    # With setting up the clock we ensure that our game speed is the same on different computers
    # with slow or fast processors.
    clock.tick(FPS)

    draw(WINDOW, images_to_draw, computer_car, player_car)

    for event in pygame.event.get():
        # Quit game
        if event.type == pygame.QUIT:
            is_running = False
            break

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            computer_car.path.append(mouse_position)

    move_player_car(player_car)
    computer_car.move()

    handle_cars_collision(computer_car, player_car, TRACK_BORDER_MASK, FINISH_LINE_MASK)

pygame.quit()
