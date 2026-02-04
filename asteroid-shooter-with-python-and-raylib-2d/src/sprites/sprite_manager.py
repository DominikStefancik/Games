from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import ImageAsset
from settings import (
    check_collision_circles,
    check_collision_circle_rec,
    close_window,
    draw_texture_ex,
    get_frame_time,
    Vector2,
    WHITE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH  ,
)
from timer import Timer

from .constants import ASTEROID_CREATION_TIMER_DURATION
from .explosion_animation import ExplosionAnimation
from .helpers import create_asteroid, create_stars_data
from .spaceship import Spaceship


class SpriteManager:
    def __init__(self):
        self.asset_manager = get_asset_manager()
        self.asteroid_sprites = []
        self.laser_sprites = []
        self.explosion_sprites = []
        self.spaceship = Spaceship(
            group=[],
            texture=self.asset_manager.textures[ImageAsset.SPACESHIP],
            position=Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2),
            laser_sprites=self.laser_sprites,
        )
        self.asteroid_timer = Timer(
            duration=ASTEROID_CREATION_TIMER_DURATION,
            repeat=True,
            autostart=True,
            function=lambda: create_asteroid(self.asteroid_sprites),
        )

        self.star_data = create_stars_data()

    def draw_stars(self):
        for star in self.star_data:
            # With the function "draw_texture_ex" we can set a texture's rotation and a scale
            draw_texture_ex(
                self.asset_manager.textures[ImageAsset.STAR], star[0], 0, star[1], WHITE
            )

    def get_all_sprites(self):
        return (
            [self.spaceship]
            + self.asteroid_sprites
            + self.laser_sprites
            + self.explosion_sprites
        )

    def update(self):
        delta_time = get_frame_time()
        self.asteroid_timer.update()

        for sprite in self.get_all_sprites():
            sprite.update(delta_time)

        self.detect_collisions()
        self.remove_sprites()

    def draw(self):
        self.draw_stars()

        for sprite in self.get_all_sprites():
            sprite.draw()

    def remove_sprites(self):
        self.remove_sprites_from_group(self.asteroid_sprites)
        self.remove_sprites_from_group(self.laser_sprites)
        self.remove_sprites_from_group(self.explosion_sprites)

    def remove_sprites_from_group(self, group):
        for index, sprite in enumerate(group):
            if sprite.to_be_removed:
                group.pop(index)

    def detect_collisions(self):
        # Spaceship and asteroids
        for asteroid in self.asteroid_sprites:
            if check_collision_circles(
                self.spaceship.get_center(),
                self.spaceship.collision_radius,
                asteroid.get_center(),
                asteroid.collision_radius,
            ):
                close_window()

        # Lasers and asteroids
        for laser in self.laser_sprites:
            for asteroid in self.asteroid_sprites:
                if check_collision_circle_rec(
                    asteroid.get_center(),
                    asteroid.collision_radius,
                    laser.get_rectangle(),
                ):
                    laser.to_be_removed = True
                    asteroid.to_be_removed = True
                    explosion = ExplosionAnimation(
                        self.asset_manager.textures[ImageAsset.EXPLOSION],
                        asteroid.position,
                    )
                    self.explosion_sprites.append(explosion)
