import constants
import pygame

import math

class Turret(pygame.sprite.Sprite):
    def __init__(self, sprite_sheets, tile_x, tile_y) -> None:
        # We have to call the superclass' init method
        pygame.sprite.Sprite.__init__(self)

        # Position variables
        self.tile_x = tile_x
        self.tile_y = tile_y
        # The calculation of X and Y coordinates is done so the turret is placed
        # in the middle of a tile
        self.x = (self.tile_x + 0.5) * constants.TILE_SIZE
        self.y = (self.tile_y + 0.5) * constants.TILE_SIZE

        self.upgrade_level = 1
        self.fire_range_radius = constants.TURRET_DATA[self.upgrade_level - 1].get("range")
        self.cooldown_interval = constants.TURRET_DATA[self.upgrade_level - 1].get("cooldown_interval")
        self.last_fired_shot_time = pygame.time.get_ticks()

        # Animation variables
        #
        # The property "sprite_sheets" contains sprites for all possible turret levels
        # Then, depending on the "upgrade_level" it will load individual frame images from a particular spritesheet
        self.sprite_sheets = sprite_sheets
        self.animation_frames = self.load_images()
        self.animation_frame_index = 0
        self.update_animation_time = pygame.time.get_ticks()

        # Update image
        self.angle = 90
        self.original_image = self.animation_frames[self.animation_frame_index]
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.is_selected = False
        self.target = None

        self.create_range_circle()

    # Loads individual frame images out of a sprite sheet
    def load_images(self):
        sprite_sheet = self.sprite_sheets[self.upgrade_level - 1]
        frame_size = sprite_sheet.get_height()
        animation_frames = []

        for index in range(constants.TURRET_ANIMATION_FRAMES):
            # The "subsurface" method extracts a section of an image
            # We need to pass top-left coordinates where the subsection starts and then wight and height of the section
            subsection_image = sprite_sheet.subsurface(index * frame_size, 0, frame_size, frame_size)
            animation_frames.append(subsection_image)

        return animation_frames

    def update(self, enemy_group):
        # If target is picked, play the firing animation
        if self.target:
            self.play_animation()
        # Otherwise search for a new target once the turret cooled down
        elif pygame.time.get_ticks() - self.last_fired_shot_time > self.cooldown_interval:
            self.pick_target(enemy_group)

    # We have to ovewrite the "draw" method from Sprite, because that one only draws the turret image,
    # but not the range cirle we want to be drawn as well
    def draw(self, surface):
        # Draw the turret image based on the original image and its rotation
        # In PyGame coordinate system we have to subtract 90 from the angle in order the turret point up
        self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        surface.blit(self.image, self.rect)
        if self.is_selected:
            surface.blit(self.range_image, self.range_rectangle)

    # Creates a transparent circle showing fire range
    def create_range_circle(self):
        self.range_image = pygame.Surface((self.fire_range_radius * 2, self.fire_range_radius * 2))
        self.range_image.fill((0,0,0))
        self.range_image.set_colorkey((0,0,0))
        pygame.draw.circle(self.range_image, "grey100", (self.fire_range_radius, self.fire_range_radius), self.fire_range_radius)
        self.range_image.set_alpha(100)
        self.range_rectangle = self.range_image.get_rect()
        # Position the circle image on top of the turret image
        self.range_rectangle.center = self.rect.center

    def play_animation(self):
        self.original_image = self.animation_frames[self.animation_frame_index]

        # Check if enough time has passed since the last frame update
        if pygame.time.get_ticks() - self.update_animation_time > constants.TURRET_ANIMATION_STEP_INTERVAL:
            self.update_animation_time = pygame.time.get_ticks()
            self.animation_frame_index += 1

            if self.animation_frame_index == len(self.animation_frames):
                self.animation_frame_index = 1

                # When the animation finishes, record completed time and clear target so cooldown interval can begin
                self.last_fired_shot_time = pygame.time.get_ticks()
                # and also set target to None, so we can start picking a target again
                self.target = None

    def pick_target(self, enemy_group):
        # Find enemy to target
        distance_x = 0
        distance_y = 0

        # Check distance to each enemy to see if it is in range
        for enemy in enemy_group:
            distance_x = enemy.current_position[0] - self.x
            distance_y = enemy.current_position[1] - self.y
            distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

            if distance < self.fire_range_radius:
                self.target = enemy
                # Calculate angle depending on where the target is
                self.angle = math.degrees(math.atan2(-distance_y, distance_x))

    def upgrade(self):
        self.upgrade_level += 1
        self.fire_range_radius = constants.TURRET_DATA[self.upgrade_level - 1].get("range")
        self.cooldown_interval = constants.TURRET_DATA[self.upgrade_level - 1].get("cooldown_interval")

        # Upgrade turret image
        self.animation_frames = self.load_images()
        self.original_image = self.animation_frames[self.animation_frame_index]

        # Since we have upgraded the range, we have to recreate the range circle
        self.create_range_circle()
