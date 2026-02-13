from settings import draw_model_ex, draw_model_wires_ex, GREEN, Vector3, WHITE, YELLOW

from .constants import MODEL_SCALE, OUTLINE_SCALE
from .board.constants import TILE_FALL_SPEED


class Model:
    def __init__(
        self,
        group,
        model,
        type,
        position,
        rotation_axis=Vector3(),
        rotation_angle=0,
        scale=Vector3(MODEL_SCALE, MODEL_SCALE, MODEL_SCALE),
        fall_position_z=None
    ):
        self.model = model
        self.type = type
        self.position = position
        self.rotation_axis = rotation_axis
        self.rotation_angle = rotation_angle
        self.scale = scale
        self.is_selected = False
        self.is_matched = False
        self.to_be_removed = False
        self.fall_position_z = self.position.z

        if fall_position_z:
            self.fall_position_z = fall_position_z


        group.append(self)

    def draw(self):
        if self.is_selected or self.is_matched:
            draw_model_wires_ex(
                self.model,
                self.position,
                self.rotation_axis,
                self.rotation_angle,
                Vector3(OUTLINE_SCALE, OUTLINE_SCALE, OUTLINE_SCALE),
                YELLOW if self.is_selected else GREEN,
            )

        draw_model_ex(
            self.model,
            self.position,
            self.rotation_axis,
            self.rotation_angle,
            self.scale,
            WHITE,
        )

    def update(self):
        if self.fall_position_z < self.position.z:
            self.position.z -= TILE_FALL_SPEED

            if self.fall_position_z > self.position.z:
                self.fall_position_z = self.position.z
