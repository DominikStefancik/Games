from random import choice, randint

from settings import pygame, TILE_SIZE, WINDOW_HEIGHT, WINDOW_WIDTH
from sprites.cloud import Cloud
from sprites.sprite import Sprite
from timer import Timer

from .constants import CameraBorder


class Background:
    def __init__(
        self,
        all_sprites_group,
        level_width,
        level_height,
        small_cloud_surfaces,
        large_cloud_surface,
        horizon_line,
        level_background_tile=None,
        top_limit=0,
    ):
        self.all_sprites_group = all_sprites_group
        self.display_surface = pygame.display.get_surface()
        # The "level_width" and "level_height" represent number of tiles and in a row and a column respectively
        # (these numbers come from Tile)
        # However, to calculate the size of the map, we have to convert them to pixels
        self.width, self.height = level_width * TILE_SIZE, level_height * TILE_SIZE

        self.draw_sky = not level_background_tile
        self.horizon_line = horizon_line

        if self.draw_sky:
            self.large_cloud = large_cloud_surface
            self.small_clouds = small_cloud_surfaces
            self.cloud_direction = -1

            self.large_cloud_speed = 50
            self.large_cloud_x = 0
            self.large_cloud_width, self.large_cloud_height = (
                self.large_cloud.get_size()
            )
            # Represents how many large cloud images do we need to fill the entire level map width
            self.large_cloud_tiles = int(self.width / self.large_cloud.get_width()) + 2
            # Run the timer repeatedly and call the given function for creating small clouds
            self.small_clouds_timer = Timer(5000, self.draw_small_cloud, True)
            self.small_clouds_timer.activate()

            for index in range(5):
                self.draw_small_cloud()
        else:
            for column in range(level_width):
                # Because the "top_limit"  is in pixels whereas the "level_height" in tiles,
                # we have to convert the "top_limit" by the tile size.
                # Since we take the camera offset into account, we have to use the negative value of top limit.
                for row in range(-int(top_limit / TILE_SIZE) - 1, level_height):
                    x, y = column * TILE_SIZE, row * TILE_SIZE
                    Sprite(
                        groups=self.all_sprites_group,
                        surface=level_background_tile,
                        position=(x, y),
                        # With the Z-index set to "-1", sprites will be drawn very first before all other sprites
                        z_index=-1,
                    )

    def draw_sky_background(self):
        self.display_surface.fill("#ddc5a1")
        horizon_position = self.horizon_line + self.all_sprites_group.offset.y
        sea_rect = pygame.FRect(
            0, horizon_position, WINDOW_WIDTH, WINDOW_HEIGHT - horizon_position
        )
        pygame.draw.rect(self.display_surface, "#92a9ce", sea_rect)

        # Horizon line visually separating the sky and the sea rectangle
        pygame.draw.line(
            self.display_surface,
            "#f5f1de",
            (0, horizon_position),
            (WINDOW_WIDTH, horizon_position),
            4,
        )

    def draw_large_cloud(self, delta_time):
        self.large_cloud_x += self.cloud_direction * self.large_cloud_speed * delta_time

        # If the whole large cloud image moved out of the screen,
        # its left coordinate will be negative value of its width
        if self.large_cloud_x <= -self.large_cloud_width:
            self.large_cloud_x = 0

        for cloud in range(self.large_cloud_tiles):
            left = (
                self.large_cloud_x
                + self.large_cloud_width * cloud
                + self.all_sprites_group.offset.x
            )
            top = (
                # We want to position the large cloud above the horizon line
                self.horizon_line
                - self.large_cloud_height
                + self.all_sprites_group.offset.y
            )
            self.display_surface.blit(self.large_cloud, (left, top))

    def draw_small_cloud(self):
        cloud_surface = choice(self.small_clouds)
        x = randint(0, self.width)
        y = randint(
            self.all_sprites_group.camera_border[CameraBorder.TOP], self.horizon_line
        )
        Cloud(self.all_sprites_group, cloud_surface, (x, y))

    def draw(self, delta_time):
        if self.draw_sky:
            # The cloud timer will only exist if we are drawing sky in a current level
            self.small_clouds_timer.update()
            self.draw_sky_background()
            self.draw_large_cloud(delta_time)
