from settings import draw_model_ex, Vector3, WHITE


class Model:
    def __init__(
        self,
        group,
        model,
        position,
        rotation_axis=Vector3(),
        rotation_angle=0,
        scale=Vector3(2, 2, 2),
    ):
        self.model = model
        self.position = position
        self.rotation_axis = rotation_axis
        self.rotation_angle = rotation_angle
        self.scale = scale
        self.to_be_removed = False

        group.append(self)

    def draw(self):
        draw_model_ex(
            self.model,
            self.position,
            self.rotation_axis,
            self.rotation_angle,
            self.scale,
            WHITE,
        )
