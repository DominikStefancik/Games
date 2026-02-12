from asset_manager.constants import FLOOR_MODEL
from settings import (
    gen_mesh_cube,
    load_model_from_mesh,
    MATERIAL_MAP_ALBEDO,
    set_material_texture,
    Vector3,
)

from .constants import FLOOR_VERTICAL_VALUE
from .model import Model


class Floor(Model):
    def __init__(self, group, texture):
        model = load_model_from_mesh(gen_mesh_cube(32, 1, 32))
        set_material_texture(model.materials[0], MATERIAL_MAP_ALBEDO, texture)

        super().__init__(
            group, model, FLOOR_MODEL, Vector3(6.5, FLOOR_VERTICAL_VALUE, -8)
        )
