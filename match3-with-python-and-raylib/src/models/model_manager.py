from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import ModelAsset, TextureAsset
from settings import (
    BoundingBox,
    check_collision_box_sphere,
    check_collision_spheres,
    get_frame_time,
    get_mesh_bounding_box,
    play_sound,
    Vector3Add,
)

from .board import Board
from .floor import Floor


class ModelManager:
    def __init__(self):
        self.asset_manager = get_asset_manager()
        self.all_models = []
        Board(self.all_models)
        Floor(self.all_models, self.asset_manager.textures[TextureAsset.BACKGROUND])

    def update(self):
        self.remove_sprites()

    def remove_sprites(self):
        self.all_models = [
            model for model in self.all_models if not model.to_be_removed
        ]

    def draw(self):
        for model in self.all_models:
            model.draw()
