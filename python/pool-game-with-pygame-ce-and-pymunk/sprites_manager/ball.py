class Ball:
    def __init__(
        self,
        shape,
        image,
    ) -> None:
        self.shape = shape
        self.image = image
        self.rect = self.image.get_frect()
        self.rect.center = (
            self.shape.body.position[0] - self.shape.radius,
            self.shape.body.position[1] - self.shape.radius,
        )

    def draw(self, surface):
        surface.blit(
            self.image,
            (
                self.shape.body.position[0] - self.shape.radius,
                self.shape.body.position[1] - self.shape.radius,
            ),
        )
