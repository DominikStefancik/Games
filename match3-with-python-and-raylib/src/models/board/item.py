from settings import draw_model_ex, draw_model_wires_ex, GREEN, Vector3, WHITE, YELLOW

from .constants import (
    BOARD_OFFSET,
    ITEM_SCALE,
    ITEM_VERTICAL_VALUE,
    OUTLINE_SCALE,
    TILE_FALL_SPEED,
    TILE_SIZE,
)
from ..model import Model


class Item(Model):
    def __init__(
        self,
        group,
        model,
        type,
        grid_position,
        rotation_axis=Vector3(),
        rotation_angle=0,
        scale=Vector3(ITEM_SCALE, ITEM_SCALE, ITEM_SCALE),
        fall_position_z=None,
    ):
        super().__init__(
            group,
            model,
            Vector3(
                BOARD_OFFSET.x - (grid_position.x * TILE_SIZE),
                ITEM_VERTICAL_VALUE,
                BOARD_OFFSET.z - (grid_position.y * TILE_SIZE),
            ),
            rotation_axis,
            rotation_angle,
            scale,
        )

        self.type = type
        self.is_selected = False
        self.is_matched = False
        self.fall_position_z = self.position.z

        if fall_position_z:
            self.fall_position_z = fall_position_z

    def is_updating_position(self):
        return self.fall_position_z != self.position.z

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
