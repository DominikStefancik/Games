from settings import MATERIAL_MAP_ALBEDO, set_material_texture, Vector3

from .constants import LASER_SPEED
from .model import Model


class Laser(Model):
    def __init__(self, group, model, texture, position):
        # Laser will always go one direction, up vertically.
        # That's why we set "Vector3(0, 0, -1)"
        super().__init__(group, model, position, LASER_SPEED, Vector3(0, 0, -1))
        set_material_texture(model.materials[0], MATERIAL_MAP_ALBEDO, texture)
