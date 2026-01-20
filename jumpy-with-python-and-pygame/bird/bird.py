import random
import pygame

from constants import BLACK, WINDOW_HEIGHT, WINDOW_WIDTH
from .constants import BIRD_ANIMATION_COOLDOWM, BIRD_FRAMES_COUNT, BIRD_FRAME_SIZE, BIRD_MOVEMENT_LEFT_TO_RIGHT, BIRD_MOVEMENT_RIGHT_TO_LEFT

class Bird(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet, y_position, scale, is_rotating):
        pygame.sprite.Sprite.__init__(self)

        self.animation_frame_list = []
        self.frame_index = 0
        self.animation_time = pygame.time.get_ticks()

        self.movement_direction = random.choice([BIRD_MOVEMENT_RIGHT_TO_LEFT, BIRD_MOVEMENT_LEFT_TO_RIGHT])
        self.flip = False

        self.process_sprite_sheet(sprite_sheet, scale)

        # Select starting frame and create a rectangle from it
        self.image = self.animation_frame_list[self.frame_index]
        self.rect = self.image.get_rect()
        # The value of "self.is_rotating" determines if the bird will move back and forth
        # when reaching the edge of the window
        # If it is false, it will disappear after it reaches the edge.
        self.is_rotating = is_rotating

        if self.movement_direction == 1:
            self.rect.x = 0
        else:
            self.rect.x = WINDOW_WIDTH

        self.rect.y = y_position

    def process_sprite_sheet(self, sprite_sheet, scale):
        for animation_frame in range(BIRD_FRAMES_COUNT):
            frame = sprite_sheet.get_frame_image(animation_frame, BIRD_FRAME_SIZE, BIRD_FRAME_SIZE, scale, BLACK)
            frame = pygame.transform.flip(frame, self.flip, False)
            frame.set_colorkey(BLACK)
            self.animation_frame_list.append(frame)

    def update(self, scroll):
        self.flip = self.movement_direction == 1

        # Update animation
        # Update image depending on the current frame
        self.image = self.animation_frame_list[self.frame_index]
        self.image = pygame.transform.flip(self.image, self.flip, False)
        self.image.set_colorkey(BLACK)

        # Check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.animation_time > BIRD_ANIMATION_COOLDOWM:
            self.animation_time = pygame.time.get_ticks()
            self.frame_index += 1

            # If the animation frames run out, start from the beginning
            if self.frame_index == len(self.animation_frame_list):
                self.frame_index = 0

        # Move the bird
        self.rect.x += self.movement_direction * 2
        # Update bird's vertical position depending on if we scroll the window or not
        self.rect.y += scroll


        if self.is_rotating:
            reached_left_edge = self.movement_direction == -1 and self.rect.left < 0
            reached_right_edge = self.movement_direction == 1 and self.rect.right > WINDOW_WIDTH
            # Check if the bird has reached the edge with the facing side
            if reached_left_edge or reached_right_edge:
                self.movement_direction *= -1

        else:
            # Check if the bird has reached the edge with other than the facing side
            if self.rect.right < 0 or self.rect.left > WINDOW_WIDTH:
                self.kill()

        # If the bird has gone off the window screen, destroy the object and remove it from the memory.
        # By doing that, it will also be removed from the "bird_group".
        # This way we achieve there will be infinite number of enemies generated, because those which
        # will go off the screen will be destroyed.
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()
