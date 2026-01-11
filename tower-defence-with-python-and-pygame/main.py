import json

import constants
import pygame
from enemy import Enemy
from helpers import create_turret
from world import World

# Initialise PyGame
pygame.init()

# Create a clock to limit the frame rate
clock = pygame.time.Clock()

# Create a game window
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Python Tower Defence")

# Load images
#
# The map was created in the program "Tiled", from which the metadata in the form of JSON has been provided
map_image = pygame.image.load(constants.MAP_PATH).convert_alpha()
# Individual turret image for mouse cursor
cursor_turret = pygame.image.load(constants.CURSOR_TURRET_PATH).convert_alpha()
enemy_image = pygame.image.load(constants.ENEMY_1_PATH).convert_alpha()

# Load JSON data for level. The json file contains waypoints
with open(constants.MAP_METADATA_PATH) as json_file:
    world_metadata = json.load(json_file)

world = World(map_image, world_metadata)

# Create groups
# Groups are provided by PyGame and help us organise objects into groups
# Then we can apply functions on all of the objects of a particular group.
# Groups functionality is similar to Python's native lists
enemy_group = pygame.sprite.Group()
turret_group = pygame.sprite.Group()

enemy = Enemy(enemy_image, world.waypoints)
enemy_group.add(enemy)

is_running = True
# Game loop
while is_running:
    # 60 frames per second
    clock.tick(constants.FPS)

    # We have to call the "fill" method so we can render over the objects (and their position)
    # which where rendered in a previous loop
    screen.fill("grey100")

    # Draw the level map
    world.draw(screen)

    # Update groups
    #
    # The "update()" method calls the "update" method on the enemy objects,
    # which inherited it from the Sprite superclass and then overwrote it
    enemy_group.update()

    # Draw groups
    #
    # The "draw()" method adds objects of a group to something like a queue
    # It calls the "draw" method on the enemy objects, which inherited it from the Sprite superclass
    enemy_group.draw(screen)
    turret_group.draw(screen)

    # Event handler
    # Events in PyGame are "stored" in an vent queue
    for event in pygame.event.get():
        # Quit program
        if event.type == pygame.QUIT:
            is_running = False

        # Handle mouse click event
        # "event.button == 1" represents the left mose button
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_position = pygame.mouse.get_pos()
            # Check that the click happened when mouse cursor was over the map area
            # as we want to add a turret to the map if the mouse cursor over it
            if (
                mouse_position[0] < constants.SCREEN_WIDTH
                and mouse_position[1] < constants.SCREEN_HEIGHT
            ):
                create_turret(cursor_turret, mouse_position, world, turret_group)

    # Update display
    # Takes all of the changes from a "queue" and displays them
    pygame.display.flip()

pygame.quit()
