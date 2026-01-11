import json

import constants
import pygame
from button import Button
from enemy import Enemy
from helpers import create_turret
from world import World

# Initialise PyGame
pygame.init()

# Create a clock to limit the frame rate
clock = pygame.time.Clock()

# Create a game window
screen = pygame.display.set_mode((constants.MAP_WIDTH + constants.SIDE_PANEL_WIDTH, constants.MAP_HEIGHT))
pygame.display.set_caption("Python Tower Defence")

# Game variables
is_placing_turrets = False

# Load images
#
# The map was created in the program "Tiled", from which the metadata in the form of JSON has been provided
map_image = pygame.image.load(constants.MAP_PATH).convert_alpha()
# Individual turret image for mouse cursor
cursor_turret = pygame.image.load(constants.CURSOR_TURRET_PATH).convert_alpha()
turret_1_sheet = pygame.image.load(constants.TURRET_1_SHEET_PATH).convert_alpha()
enemy_image = pygame.image.load(constants.ENEMY_1_PATH).convert_alpha()
buy_turret_image = pygame.image.load(constants.BUY_TURRET_PATH).convert_alpha()
cancel_image = pygame.image.load(constants.CANCEL_PATH).convert_alpha()

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

buy_turret_button = Button(buy_turret_image, constants.MAP_WIDTH + 30, 120, True)
cancel_button = Button(cancel_image, constants.MAP_WIDTH + 50, 180, True)

is_running = True
# Game loop
while is_running:
    # 60 frames per second
    clock.tick(constants.FPS)

    ########################
    #   UPDATING SECTION   #
    ########################

    # Update groups
    #
    # The "update()" method calls the "update" method on the enemy objects,
    # which inherited it from the Sprite superclass and then overwrote it
    enemy_group.update()
    turret_group.update()

    #######################
    #   DRAWING SECTION   #
    #######################

    # We have to call the "fill" method so we can render over the objects (and their position)
    # which where rendered in a previous loop
    screen.fill("grey100")

    # Draw the level map
    world.draw(screen)



    # Draw groups
    #
    # The "draw()" method adds objects of a group to something like a queue
    # It calls the "draw" method on the enemy objects, which inherited it from the Sprite superclass
    enemy_group.draw(screen)
    turret_group.draw(screen)

    if buy_turret_button.draw(screen):
        is_placing_turrets = True

    # If user is placing turrets, then whow the Cancel button as well
    if is_placing_turrets:
        # Show cursor as a turret image
        cursor_rectangle = cursor_turret.get_rect()
        cursor_position = pygame.mouse.get_pos()
        cursor_rectangle.center = cursor_position

        # Show the turret cursor only when the cursor is over the map area
        if cursor_position[0] < constants.MAP_WIDTH:
            screen.blit(cursor_turret, cursor_rectangle)

        if cancel_button.draw(screen):
            is_placing_turrets = False

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
                mouse_position[0] < constants.MAP_WIDTH
                and mouse_position[1] < constants.MAP_HEIGHT
            ):
                if is_placing_turrets:
                    create_turret(turret_1_sheet, mouse_position, world, turret_group)

    # Update display
    # Takes all of the changes from a "queue" and displays them
    pygame.display.flip()

pygame.quit()
