import constants
import pygame


class Turret(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet, tile_x, tile_y) -> None:
        # We have to call the superclass' init method
        pygame.sprite.Sprite.__init__(self)

        # Position variables
        self.tile_x = tile_x
        self.tile_y = tile_y
        # The calculation of X and Y coordinates is done so the turret is placed
        # in the middle of a tile
        self.x = (self.tile_x + 0.5) * constants.TILE_SIZE
        self.y = (self.tile_y + 0.5) * constants.TILE_SIZE

        self.cooldown = 1500
        self.last_fired_shot_time = pygame.time.get_ticks()

        # Animation variables
        self.sprite_sheet = sprite_sheet
        self.animation_frames = self.load_images()
        self.animation_frame_index = 0
        self.update_animation_time = pygame.time.get_ticks()

        # Update image
        self.image = self.animation_frames[self.animation_frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    # Loads individual frame images out of a sprite sheet
    def load_images(self):
        frame_size = self.sprite_sheet.get_height()
        animation_frames = []

        for index in range(constants.TURRET_ANIMATION_FRAMES):
            # The "subsurface" method extracts a section of an image
            # We need to pass top-left coordinates where the subsection starts and then wight and height of the section
            subsection_image = self.sprite_sheet.subsurface(index * frame_size, 0, frame_size, frame_size)
            animation_frames.append(subsection_image)

        return animation_frames

    def update(self):
        # Search for a new target once the turret cooled down
        if pygame.time.get_ticks() - self.last_fired_shot_time > self.cooldown:
            self.play_animation()

    def play_animation(self):
        self.image = self.animation_frames[self.animation_frame_index]

        # Check if enough time has passed since the last frame update
        if pygame.time.get_ticks() - self.update_animation_time > constants.TURRET_ANIMATION_STEP_INTERVAL:
            self.update_animation_time = pygame.time.get_ticks()
            self.animation_frame_index += 1

            if self.animation_frame_index == len(self.animation_frames):
                self.animation_frame_index = 1

                # When the animation finishes record completed time and clear target so cooldown can begin
                self.last_fired_shot_time = pygame.time.get_ticks()
