from settings import Z_Layer

from .spiked_ball import SpikedBall


class SpikedChain(SpikedBall):
    def __init__(
        self, groups, surface, position, radius, start_angle, end_angle, speed, z_index
    ):
        super().__init__(
            groups, surface, position, radius, start_angle, end_angle, speed, z_index
        )
