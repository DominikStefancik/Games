from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import ModelAsset, TextureAsset
from settings import get_frame_time
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

    def draw(self):
        for model in self.get_all_models():
            model.draw()
