from os.path import join

from settings import pygame, vector, TILE_SIZE, Z_Layer
from timer import Timer

from .constants import (
    Collision,
    PLAYER_GRAVITY,
    PLAYER_JUMP_HEIGHT,
    PLAYER_SPEED,
    PlayerTimerType,
    SurfaceContact,
)


class Player(pygame.sprite.Sprite):
    def __init__(self, groups, position, collision_sprites, semi_collision_sprites):
        super().__init__(groups)
        self.image = pygame.image.load(
            join("assets", "graphics", "player", "idle", "0.png")
        )
        # Represents a rectangle to figure out where the player will be drawn in a current frame
        self.rect = self.image.get_frect(topleft=position)
        # The method "inflate" takes a rectangle and resizes it with keeping its origin center point
        # In our case, the hitbox will be of a smaller size because we provided negative numbers
        self.hitbox_rect = self.rect.inflate(-76, -36)
        # Represents a rectangle to figure out where the player was drawn in a previous frame
        self.previous_rect = self.hitbox_rect.copy()
        self.z_index = Z_Layer.MAIN.value

        self.direction = vector()
        self.speed = PLAYER_SPEED
        self.is_jumping = False
        self.is_on_surface = {
            SurfaceContact.FLOOR: False,
            SurfaceContact.LEFT: False,
            SurfaceContact.RIGHT: False,
        }

        self.collision_sprites = collision_sprites
        self.semi_collision_sprites = semi_collision_sprites
        # Represents a possible moving platform the player might be standing during the game
        self.moving_platform = None

        self.timers = {
            PlayerTimerType.WALL_JUMP: Timer(500),
            # Timer for allowing a wall jump after a short time interval
            PlayerTimerType.WALL_SLIDE_BLOCK: Timer(250),
            PlayerTimerType.PLATFORM_FALL_DOWN: Timer(300),
        }

    def process_key_input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector()

        if not self.timers[PlayerTimerType.WALL_JUMP].active:
            if keys[pygame.K_LEFT]:
                input_vector.x -= 1
            if keys[pygame.K_RIGHT]:
                input_vector.x += 1
            if keys[pygame.K_DOWN]:
                self.timers[PlayerTimerType.PLATFORM_FALL_DOWN].activate()

            # Normalise the vector only if one of its values is not zero
            self.direction.x = (
                input_vector.normalize().x if input_vector else input_vector.x
            )

        is_on_surface = any(
            [
                self.is_on_surface[SurfaceContact.FLOOR],
                self.is_on_surface[SurfaceContact.LEFT],
                self.is_on_surface[SurfaceContact.RIGHT],
            ]
        )

        if keys[pygame.K_SPACE] and is_on_surface:
            self.is_jumping = True

    def move(self, delta_time):
        self.hitbox_rect.x += self.direction.x * self.speed * delta_time
        self.detect_collision(Collision.HORIZONTAL)

        # Process vertical change
        is_on_wall = any(
            [
                self.is_on_surface[SurfaceContact.LEFT],
                self.is_on_surface[SurfaceContact.RIGHT],
            ]
        )

        if (
            not self.is_on_surface[SurfaceContact.FLOOR]
            and is_on_wall
            and not self.timers[PlayerTimerType.WALL_SLIDE_BLOCK].active
        ):
            self.direction.y = 0
            self.hitbox_rect.y += PLAYER_GRAVITY / 10 * delta_time
        else:
            # The longer the player keeps falling, the bigger the gravity is and the faster he falls
            self.direction.y += PLAYER_GRAVITY / 2 * delta_time
            self.hitbox_rect.y += self.direction.y * delta_time
            self.direction.y += PLAYER_GRAVITY / 2 * delta_time

        self.detect_collision(Collision.VERTICAL)
        self.detect_semi_collision()

        if self.is_jumping:
            if self.is_on_surface[SurfaceContact.FLOOR]:
                self.direction.y = -PLAYER_JUMP_HEIGHT
                # After the player jumps of the floor, he should not be able to immediately jump of the wall
                self.timers[PlayerTimerType.WALL_SLIDE_BLOCK].activate()
            if is_on_wall and not self.timers[PlayerTimerType.WALL_SLIDE_BLOCK].active:
                self.timers[PlayerTimerType.WALL_JUMP].activate()
                self.direction.y = -PLAYER_JUMP_HEIGHT
                self.direction.x = 1 if self.is_on_surface[SurfaceContact.LEFT] else -1

            self.is_jumping = False

        # self.detect_collision(Collision.VERTICAL)
        # self.detect_semi_collision()
        self.rect.center = self.hitbox_rect.center

    # Updates the player's position if he stands on a moving platform
    def move_with_platform(self, delta_time):
        if self.moving_platform:
            self.hitbox_rect.topleft += (
                self.moving_platform.direction * self.moving_platform.speed * delta_time
            )

            if self.hitbox_rect.bottom >= self.moving_platform.rect.top:
                self.hitbox_rect.bottom = self.moving_platform.rect.top

    def check_contact_with_surface(self):
        # Create tiny invisible rectangles on the player's sides which will be used for collision detection
        floor_rectangle = pygame.Rect(
            self.hitbox_rect.bottomleft, (self.hitbox_rect.width, 2)
        )
        left_rectangle = pygame.Rect(
            self.hitbox_rect.topleft + vector(-2, self.hitbox_rect.height / 4),
            (2, self.hitbox_rect.height / 2),
        )
        right_rectangle = pygame.Rect(
            self.hitbox_rect.topright + vector(0, self.hitbox_rect.height / 4),
            (2, self.hitbox_rect.height / 2),
        )
        collision_rectangles = [sprite.rect for sprite in self.collision_sprites]
        semi_collision_rectangles = [
            sprite.rect for sprite in self.semi_collision_sprites
        ]

        # The method "collidelist()" checks if the given rectangle collides with any of sprites provided
        # in the list argument. Returns an index of the sprite with which the given rectangle collides.
        # If the return value is -1, it doesn't collide with any of the sprites from the list.
        self.is_on_surface[SurfaceContact.FLOOR] = (
            floor_rectangle.collidelist(collision_rectangles) >= 0
            or floor_rectangle.collidelist(semi_collision_rectangles) >= 0
        )
        self.is_on_surface[SurfaceContact.LEFT] = (
            left_rectangle.collidelist(collision_rectangles) >= 0
        )
        self.is_on_surface[SurfaceContact.RIGHT] = (
            right_rectangle.collidelist(collision_rectangles) >= 0
        )

        self.moving_platform = None
        collidable_sprites = (
            self.collision_sprites.sprites() + self.semi_collision_sprites.sprites()
        )
        # Check if the player landed on a moving platform
        # We iterate through collision sprites but are interested only in those which are moving
        for sprite in [sprite for sprite in collidable_sprites if sprite.is_moving]:
            if sprite.rect.colliderect(floor_rectangle):
                self.moving_platform = sprite

    def detect_collision(self, collision_axis):
        # For processing collisions we want to separate horizontal and vertical axes
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if collision_axis == Collision.HORIZONTAL:
                    # Collision happened from the left side of the player to the right side of the sprite
                    # where the player was on the right side of the sprite before the collision
                    if self.hitbox_rect.left <= sprite.rect.right and int(
                        self.previous_rect.left
                    ) >= int(sprite.previous_rect.right):
                        self.hitbox_rect.left = sprite.rect.right

                    # Collision happened from the right side of the player to the left side of the sprite
                    # where the player was on the left side of the sprite before the collision
                    if self.hitbox_rect.right >= sprite.rect.left and int(
                        self.previous_rect.right
                    ) <= int(sprite.previous_rect.left):
                        self.hitbox_rect.right = sprite.rect.left

                if collision_axis == Collision.VERTICAL:
                    # Collision happened from the top side of the player to the bottom side of the sprite
                    # where the player was on the bottom side of the sprite before the collision
                    if self.hitbox_rect.top <= sprite.rect.bottom and int(
                        self.previous_rect.top
                    ) >= int(sprite.previous_rect.bottom):
                        self.hitbox_rect.top = sprite.rect.bottom

                        # In the case of the moving platform going down and the player jumping up
                        # we want to give him some offset, otherwise he is stuck to the bottom part of the platform.
                        if sprite.is_moving:
                            self.hitbox_rect.top += 20

                    # Collision happened from the bottom side of the player to the top side of the sprite
                    # where the player was on the top side of the sprite before the collision
                    if self.hitbox_rect.bottom >= sprite.rect.top and int(
                        self.previous_rect.bottom
                    ) <= int(sprite.previous_rect.top):
                        self.hitbox_rect.bottom = sprite.rect.top

                    # If a vertical collision happened, we want to reset the vertical direction
                    # otherwise, the gravity would keep applying even though the player is not falling
                    self.direction.y = 0

    def detect_semi_collision(self):
        if not self.timers[PlayerTimerType.PLATFORM_FALL_DOWN].active:
            for sprite in self.semi_collision_sprites:
                if sprite.rect.colliderect(self.hitbox_rect):
                    # We are only interested in collision which happened from the bottom side of the player
                    # to the top side of the sprite where the player was on the top side of the sprite
                    # before the collision.
                    if self.hitbox_rect.bottom >= sprite.rect.top and int(
                        self.previous_rect.bottom
                    ) <= int(sprite.previous_rect.top):
                        self.hitbox_rect.bottom = sprite.rect.top

                        if self.direction.y > 0:
                            self.direction.y = 0

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, delta_time):
        # Before updating the movement, store the position of the current rectangle
        # This will be then used for a collision detection
        self.previous_rect = self.hitbox_rect.copy()
        self.update_timers()
        self.process_key_input()
        self.move(delta_time)
        self.move_with_platform(delta_time)
        self.check_contact_with_surface()
