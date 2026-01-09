import constants
import pygame
from enemy import Enemy

# Initialise PyGame
pygame.init()

# Create a clock to limit the frame rate
clock = pygame.time.Clock()

# Create a game window
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Python Tower Defence")

# Load images
enemy_image = pygame.image.load(constants.ENEMY_1_PATH).convert_alpha()

# Create groups
# Groups are provided by PyGame and help us organise objects into groups
# Then we can apply functions on all of the objects of a particular group.
# Groups functionality is similar to Python's native lists
enemy_group = pygame.sprite.Group()

waypoints = [
    (100, 100),
    (400, 200),
    (400, 100),
    (200, 300),
]

enemy = Enemy(enemy_image, waypoints)
enemy_group.add(enemy)

is_running = True
# Game loop
while is_running:
    # 60 frames per second
    clock.tick(constants.FPS)

    # We have to call the "fill" method so we can render over the objects (and their position)
    # which where rendered in a previous loop
    screen.fill("grey100")

    # Draw enemy path
    pygame.draw.lines(screen, "grey0", False, waypoints)

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

    # Event handler
    # Events in PyGame are "stored" in an vent queue
    for event in pygame.event.get():
        # Quit program
        if event.type == pygame.QUIT:
            is_running = False

    # Update display
    # Takes all of the changes from a "queue" and displays them
    pygame.display.flip()

pygame.quit()
