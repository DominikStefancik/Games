from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import ModelAsset
from models.model_manager import ModelManager
from settings import (
    BACKGROUND_COLOR,
    begin_drawing,
    begin_mode_3d,
    Camera3D,
    CAMERA_PERSPECTIVE,
    clear_background,
    close_window,
    end_drawing,
    end_mode_3d,
    init_window,
    set_target_fps,
    Vector3,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    window_should_close,
)


class Game:
    def __init__(self):
        # The "init_window" function is imported from "settings.py" where there is "from pyray import *" statement
        init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Python Match3")

        # Camera setup
        self.camera = Camera3D()
        self.camera.position = Vector3(0.0, 16.0, -16.0)
        self.camera.target = Vector3(0.0, 0.0, -1.0)
        self.camera.up = Vector3(0.0, 1.0, 0.0)
        self.camera.fovy = 90.0
        self.camera.projection = CAMERA_PERSPECTIVE

        self.asset_manager = get_asset_manager()
        self.model_manager = ModelManager()

        set_target_fps(60)

    def update(self):
        self.model_manager.update()

    def draw(self):
        clear_background(BACKGROUND_COLOR)
        begin_drawing()

        begin_mode_3d(self.camera)
        self.model_manager.draw()
        end_mode_3d()

        end_drawing()

    def run(self):
        while not window_should_close():
            self.update()
            self.draw()

        close_window()


# To make sure we are running only main.py and not anything else
if __name__ == "__main__":
    game = Game()
    game.run()
