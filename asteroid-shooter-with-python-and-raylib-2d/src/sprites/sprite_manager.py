from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import ImageAsset, SoundAsset
from game_state.game_state import GameState
from game_state.game_state_manager import get_game_state_manager
from settings import (
    check_collision_circles,
    check_collision_circle_rec,
    draw_texture_ex,
    get_frame_time,
    play_sound,
    Vector2,
    WHITE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from timer import Timer

from .constants import ASTEROID_CREATION_TIMER_DURATION
from .explosion_animation import ExplosionAnimation
from .helpers import create_asteroid, create_laser, create_stars_data
from .spaceship import Spaceship


class SpriteManager:
    def __init__(self):
        self.asset_manager = get_asset_manager()
        self.asteroid_sprites = []
        self.laser_sprites = []
        self.explosion_sprites = []
        self.spaceship = None
        self.asteroid_timer = Timer(
            duration=ASTEROID_CREATION_TIMER_DURATION,
            repeat=True,
            autostart=True,
            function=lambda: create_asteroid(self.asteroid_sprites),
        )

        self.star_data = create_stars_data()

        self.game_state_manager = get_game_state_manager()
        self.game_state_manager.subscribe(self)

    def draw_stars(self):
        for star in self.star_data:
            # With the function "draw_texture_ex" we can set a texture's rotation and a scale
            draw_texture_ex(
                self.asset_manager.textures[ImageAsset.STAR], star[0], 0, star[1], WHITE
            )

    def get_all_sprites(self):
        return (
            ([self.spaceship] if self.spaceship else [])
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
        self.asteroid_sprites = [
            sprite for sprite in self.asteroid_sprites if not sprite.to_be_removed
        ]
        self.laser_sprites = [
            sprite for sprite in self.laser_sprites if not sprite.to_be_removed
        ]
        self.explosion_sprites = [
            sprite for sprite in self.explosion_sprites if not sprite.to_be_removed
        ]

    def detect_collisions(self):
        # Spaceship and asteroids
        if self.spaceship:
            for asteroid in self.asteroid_sprites:
                if check_collision_circles(
                    self.spaceship.get_center(),
                    self.spaceship.collision_radius,
                    asteroid.get_center(),
                    asteroid.collision_radius,
                ):
                    self.spaceship = None
                    self.game_state_manager.game_state = GameState.GAME_OVER
                    play_sound(
                        self.asset_manager.sounds[SoundAsset.SPACESHIP_EXPLOSION]
                    )
                    # After we detect a collision, we "destroy" spaceship and then we have to
                    # break from the FOR loop, because otherwise we will continue checking for possible
                    # collisions with other asteroids when the "self.spaceship" is set to None
                    break

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
                    play_sound(self.asset_manager.sounds[SoundAsset.ASTEROID_EXPLOSION])

    def update_items(self):
        self.asteroid_sprites = []
        self.laser_sprites = []
        self.explosion_sprites = []
        self.spaceship = Spaceship(
            group=[],
            texture=self.asset_manager.textures[ImageAsset.SPACESHIP],
            position=Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2),
            create_laser_function=lambda position: create_laser(
                self.laser_sprites, position
            ),
        )
