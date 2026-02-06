from settings import (
    gen_mesh_cube,
    load_model_from_mesh,
    MATERIAL_MAP_ALBEDO,
    set_material_texture,
    Vector3,
)

from .model import Model


class Floor(Model):
    def __init__(self, group, texture):
        model = load_model_from_mesh(gen_mesh_cube(32, 1, 32))
        set_material_texture(model.materials[0], MATERIAL_MAP_ALBEDO, texture)

        # The floor doesn't suppose to move, so the speed is 0
        super().__init__(group, model, Vector3(6.5, -2, -8), 0)
