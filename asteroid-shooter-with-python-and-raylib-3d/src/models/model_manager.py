from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import ModelAsset, SoundAsset, TextureAsset
from settings import (
    BoundingBox,
    check_collision_box_sphere,
    check_collision_spheres,
    get_frame_time,
    get_mesh_bounding_box,
    play_sound,
    Vector3Add,
)
from timer import Timer

from .constants import ASTEROID_CREATION_TIMER_DURATION
from .helpers import create_asteroid, create_laser
from .floor import Floor
from .spaceship import Spaceship


class ModelManager:
    def __init__(self):
        self.asset_manager = get_asset_manager()
        self.single_models = []
        self.asteroid_models = []
        self.laser_models = []
        Floor(self.single_models, self.asset_manager.textures[TextureAsset.DARK])
        self.spaceship = Spaceship(
            group=self.single_models,
            model=self.asset_manager.models[ModelAsset.SPACESHIP],
            create_laser_function=lambda position: create_laser(
                self.laser_models, position
            ),
        )
        self.asteroid_timer = Timer(
            duration=ASTEROID_CREATION_TIMER_DURATION,
            repeat=True,
            autostart=True,
            function=lambda: create_asteroid(self.asteroid_models),
        )

    def get_all_models(self):
        return self.single_models + self.laser_models + self.asteroid_models

    def update(self):
        delta_time = get_frame_time()
        self.asteroid_timer.update()

        for model in self.get_all_models():
            model.update(delta_time)

        self.detect_collisions()
        self.remove_sprites()

    def remove_sprites(self):
        self.asteroid_models = [
            model for model in self.asteroid_models if not model.to_be_removed
        ]
        self.laser_models = [
            model for model in self.laser_models if not model.to_be_removed
        ]

    def draw(self):
        for model in self.get_all_models():
            model.draw()

    def detect_collisions(self):
        # Spaceship and asteroids
        if self.spaceship:
            for asteroid in self.asteroid_models:
                if check_collision_spheres(
                    self.spaceship.position,
                    self.spaceship.collision_radius,
                    asteroid.position,
                    asteroid.radius,
                ):
                    self.spaceship = None
                    play_sound(
                        self.asset_manager.sounds[SoundAsset.SPACESHIP_EXPLOSION]
                    )
                    # After we detect a collision, we "destroy" spaceship and then we have to
                    # break from the FOR loop, because otherwise we will continue checking for possible
                    # collisions with other asteroids when the "self.spaceship" is set to None
                    break

        # Lasers and asteroids
        for laser in self.laser_models:
            # This bounding box doesn't have laser's position. We have to add it manually.
            laser_bounding_box = get_mesh_bounding_box(laser.model.meshes[0])
            # A collision box which has the position of the laser
            collision_box = BoundingBox(
                Vector3Add(laser_bounding_box.min, laser.position),
                Vector3Add(laser_bounding_box.max, laser.position),
            )
            for asteroid in self.asteroid_models:
                if check_collision_box_sphere(
                    collision_box,
                    asteroid.position,
                    asteroid.radius,
                ):
                    laser.to_be_removed = True
                    asteroid.is_hit = True
                    asteroid.destruction_timer.activate()
                    play_sound(self.asset_manager.sounds[SoundAsset.ASTEROID_EXPLOSION])
