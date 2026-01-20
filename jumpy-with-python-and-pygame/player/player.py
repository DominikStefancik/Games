import pygame

from constants import VERTICAL_SCROLL_THRESHOLD, WHITE, WINDOW_HEIGHT, WINDOW_WIDTH
from .constants import GRAVITY, JUMPY_BOUNCE_VELOCITY, JUMPY_IMAGE_SCALE, JUMPY_MOVEMENT_DISTANCE


class Player:
    def __init__(self, image, starting_position):
        self.image = pygame.transform.scale(image, JUMPY_IMAGE_SCALE)
        self.rect_width = 30
        self.rect_height = 40
        # Pygame uses image rectangle for setting up image's starting_position
        # and also to detect collision of the image with other objects.
        #
        # Rather than creating a rectangle from the image, we create it manually.
        # The reason is if we created it from the image with "self.image.get_rect()" Pygame would create a rectangle
        # in which the whole image would fit.
        # However, it would be too big and there would be a lot of empty space between the image and
        # some rectangle's edges. This would cause problems when detecting collisions of the image and other
        # objects.
        # The collision would be detected, even though the image and an object didn't directly visibly touched.
        self.rect = pygame.Rect(0, 0, self.rect_width, self.rect_height)
        self.rect.center = starting_position
        self.velocity_y = 0
        self.flip_image = False

    def move(self, platform_group):
        # Reset variables
        delta_x = 0
        delta_y = 0
        scroll = 0

        # Process key presses
        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT]:
            delta_x = -JUMPY_MOVEMENT_DISTANCE
            self.flip_image = True
        if key[pygame.K_RIGHT]:
            delta_x = JUMPY_MOVEMENT_DISTANCE
            self.flip_image = False

        # Every game loop iteration increase the vertical velocity
        self.velocity_y += GRAVITY
        delta_y += self.velocity_y

        # Make sure that before we update the player's position he doesn't go off the edge of the window
        if self.rect.left + delta_x < 0:
            delta_x = -self.rect.left
        if self.rect.right + delta_x > WINDOW_WIDTH:
            delta_x = WINDOW_WIDTH - self.rect.right

        # Check collision with platforms
        for platform in platform_group:
            # We are interested only in collisions in the vertical direction
            # Check if the platform's rectangle would have collided with the player's rectangle
            # after we update its position with delta_y
            if platform.rect.colliderect(self.rect.x, self.rect.y + delta_y, self.rect_width, self.rect_height):
                # Check if the bottom of the player's image has lower value than the platform vertical value
                # If that is true, it means the player is above the platform
                # (because in Pygame the Y-coordinate starts at the top left corner and increaces when going to
                # the bottom of the game window)
                if self.rect.bottom < platform.rect.centery:
                    # We have to check only if the player is falling
                    # If the "self.velocity_y" is negative number, that means the player is jumping up
                    if self.velocity_y > 0:
                        self.rect.bottom = platform.rect.top
                        delta_y = 0
                        # If the player reaches the top of the platform while falling, we want him to jump up.
                        # By setting the velocity to a negative number, each loop the "delta_y" will be lower
                        # and lower which in the end will cause the value of the "self.rect.y" to decrease
                        # and the player image will go up
                        self.velocity_y = -JUMPY_BOUNCE_VELOCITY

        # Check if the player has bounced on the top of the scrolling threshold
        # If that happens, we need to scroll everything relative to the player's vertical position
        if self.rect.top <= VERTICAL_SCROLL_THRESHOLD:
            # Only update the scroll when the player is jumping up
            if self.velocity_y < 0:
                # If the player is moving up, everything else is moving down
                scroll = -delta_y

        # Update rectangle position (and with that automatically the image position)
        self.rect.x += delta_x
        # When the window scroll should happen, we want the player to freze for a moment until the scrolling is done
        # By adding "delta_y + scroll" we get 0, in case when the window should scroll ->
        # this is how the "freeze" effect will be achieved
        self.rect.y += delta_y + scroll

        # Update mask for collision detection depending on the player's current position
        self.mask = pygame.mask.from_surface(self.image)

        return scroll


    def draw(self, surface):
        surface.blit(pygame.transform.flip(self.image, self.flip_image, False), (self.rect.x - 8, self.rect.y - 5))
