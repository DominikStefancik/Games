import json

import pygame
from button import Button
from enemy.constants import (
    ENEMY_1_PATH,
    ENEMY_2_PATH,
    ENEMY_3_PATH,
    ENEMY_4_PATH,
    SPAWN_ENEMY_COOLDOWN,
)
from enemy.enemy import Enemy
from enemy.enemy_type import EnemyType
from game_status import GameStatus
from turret.constants import (
    BUY_TURRET_COST,
    BUY_TURRET_PATH,
    CANCEL_PATH,
    CURSOR_TURRET_PATH,
    UPGRADE_TURRET_COST,
    UPGRADE_TURRET_PATH,
    TURRET_DATA,
)
from turret.helpers import (
    get_turret_spritesheet_path,
    create_turret,
    select_turret,
    clear_turret_selection,
)
from world.constants import (
    BEGIN_PATH,
    FPS,
    LEVEL_COMPLETED_REWARD,
    MAP_METADATA_PATH,
    MAP_PATH,
    MAP_HEIGHT,
    MAP_WIDTH,
    RESTART_PATH,
    SIDE_PANEL_WIDTH,
    TOTAL_LEVELS
)
from world.helpers import draw_text
from world.world import World

# Initialise PyGame
pygame.init()

# Create a clock to limit the frame rate
clock = pygame.time.Clock()

# Create a game window
screen = pygame.display.set_mode((MAP_WIDTH + SIDE_PANEL_WIDTH, MAP_HEIGHT))
pygame.display.set_caption("Python Tower Defence")

# Game variables
level_started = False
game_status = GameStatus.RUNNING
time_of_last_spawn_enemy = pygame.time.get_ticks()
is_placing_turrets = False
selected_turret = None

# Load images
#
# The map was created in the program "Tiled", from which the metadata in the form of JSON has been provided
map_image = pygame.image.load(MAP_PATH).convert_alpha()
# Individual turret image for mouse cursor
cursor_turret = pygame.image.load(CURSOR_TURRET_PATH).convert_alpha()

turret_spritesheets = []
for x in range(1, len(TURRET_DATA) + 1):
    file_path = get_turret_spritesheet_path(x)
    turret_sheet = pygame.image.load(file_path).convert_alpha()
    turret_spritesheets.append(turret_sheet)

enemy_images = {
    EnemyType.WEAK: pygame.image.load(ENEMY_1_PATH).convert_alpha(),
    EnemyType.MEDIUM: pygame.image.load(ENEMY_2_PATH).convert_alpha(),
    EnemyType.STRONG: pygame.image.load(ENEMY_3_PATH).convert_alpha(),
    EnemyType.ELITE: pygame.image.load(ENEMY_4_PATH).convert_alpha(),
}
buy_turret_image = pygame.image.load(BUY_TURRET_PATH).convert_alpha()
upgrade_turret_image = pygame.image.load(UPGRADE_TURRET_PATH).convert_alpha()
cancel_image = pygame.image.load(CANCEL_PATH).convert_alpha()
begin_image = pygame.image.load(BEGIN_PATH).convert_alpha()
restart_image = pygame.image.load(RESTART_PATH).convert_alpha()

# Load JSON data for level. The json file contains waypoints
with open(MAP_METADATA_PATH) as json_file:
    world_metadata = json.load(json_file)

# Load fonts for displaying text on the screen
text_font = pygame.font.SysFont("Consolas", 24, bold=True)
large_font = pygame.font.SysFont("Consolas", 36)

world = World(map_image, world_metadata)

# Create groups
# Groups are provided by PyGame and help us organise objects into groups
# Then we can apply functions on all of the objects of a particular group.
# Groups functionality is similar to Python's native lists
enemy_group = pygame.sprite.Group()
turret_group = pygame.sprite.Group()

buy_turret_button = Button(buy_turret_image, MAP_WIDTH + 30, 120, True)
cancel_button = Button(cancel_image, MAP_WIDTH + 50, 180, True)
upgrade_turret_button = Button(upgrade_turret_image, MAP_WIDTH + 5, 180, True)
begin_button = Button(begin_image, MAP_WIDTH + 60, 300, True)
restart_button = Button(restart_image, 310, 350, True)

is_running = True
# Game loop
while is_running:
    # 60 frames per second
    clock.tick(FPS)

    ########################
    #   UPDATING SECTION   #
    ########################

    if game_status == GameStatus.RUNNING:
        if world.health <= 0:
            game_status = GameStatus.LOSS

        # Check if player has won
        if world.level > TOTAL_LEVELS:
            game_status = GameStatus.WON

        # Update groups
        #
        # The "update()" method calls the "update" method on the enemy objects,
        # which inherited it from the Sprite superclass and then overwrote it
        enemy_group.update(world)
        turret_group.update(enemy_group)

        # Highlight selected turret
        if selected_turret:
            selected_turret.is_selected = True

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

    # Since we have overwritten the "draw" method in the Turret class, calling "turret_group.draw(screen)" still
    # calls the "draw" method on each of the turret objects in the group, but only draws the turret image, not the circle.
    # In order to draw both, we have to loop over each individual object and call the "draw" method manually.
    for turret in turret_group:
        turret.draw(screen)

    draw_text(screen, str(world.health), text_font, "grey100", 0, 0)
    draw_text(screen, str(world.money), text_font, "grey100", 0, 30)
    draw_text(screen, str(world.level), text_font, "grey100", 0, 60)

    if game_status == GameStatus.RUNNING:
        # Check if the level has been started or not
        if level_started == False:
            if begin_button.draw(screen):
                level_started = True
        else:
            # Spawn enemies:
            if pygame.time.get_ticks() - time_of_last_spawn_enemy > SPAWN_ENEMY_COOLDOWN:
                if world.spawned_enemies < len(world.enemy_type_list):
                    enemy_type = world.enemy_type_list[world.spawned_enemies]
                    enemy = Enemy(enemy_type, enemy_images, world.waypoints)
                    enemy_group.add(enemy)
                    world.spawned_enemies += 1
                    time_of_last_spawn_enemy = pygame.time.get_ticks()

        # Check if the level is finished
        if world.is_level_completed():
            level_started = False
            world.level += 1
            world.money += LEVEL_COMPLETED_REWARD
            time_of_last_spawn_enemy = pygame.time.get_ticks()
            world.reset_level()

        if buy_turret_button.draw(screen):
            is_placing_turrets = True

        # If user is placing turrets, then whow the Cancel button as well
        if is_placing_turrets:
            # Show cursor as a turret image
            cursor_rectangle = cursor_turret.get_rect()
            cursor_position = pygame.mouse.get_pos()
            cursor_rectangle.center = cursor_position

            # Show the turret cursor only when the cursor is over the map area
            if cursor_position[0] < MAP_WIDTH:
                screen.blit(cursor_turret, cursor_rectangle)

            if cancel_button.draw(screen):
                is_placing_turrets = False

        # If a turret is selected then show the Upgrade button
        if selected_turret:
            # Only if a turret can be upgraded show the Upgrade button
            if selected_turret.upgrade_level < len(TURRET_DATA):
                if upgrade_turret_button.draw(screen):
                    if world.money >= UPGRADE_TURRET_COST:
                        selected_turret.upgrade()
                        world.money -= UPGRADE_TURRET_COST
    else: # The game is not running anymore
        pygame.draw.rect(screen, "dodgerblue", (200, 250, 400, 200), border_radius = 30)

        if game_status == GameStatus.WON:
            draw_text(screen, "YOU WIN!", large_font, "grey0", 315, 280)
        elif game_status == GameStatus.LOSS:
            draw_text(screen, "GAME OVER", large_font, "grey0", 310, 280)

        # Restart game after the restart button was clicked on
        if restart_button.draw(screen):
            game_status = GameStatus.RUNNING
            level_started = False
            is_placing_turrets = False
            selected_turret = None
            time_of_last_spawn_enemy = pygame.time.get_ticks()
            # After restart, recreate the whole world from scratch
            world = World(map_image, world_metadata)
            # We need to empty the groups, so the objects are not in the memory anymore
            enemy_group.empty()
            turret_group.empty()

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
            if mouse_position[0] < MAP_WIDTH and mouse_position[1] < MAP_HEIGHT:
                selected_turret = None
                clear_turret_selection(turret_group)
                if is_placing_turrets:
                    # Check if there is enough money for a turret
                    if world.money >= BUY_TURRET_COST:
                        create_turret(
                            turret_spritesheets, mouse_position, world, turret_group
                        )
                else:
                    selected_turret = select_turret(mouse_position, turret_group)

    # Update display
    # Takes all of the changes from a "queue" and displays them
    pygame.display.flip()

pygame.quit()
