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
    Vector3,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    window_should_close,
)


class Game:
    def __init__(self):
        # The "init_window" function is imported from "settings.py" where there is "from pyray import *" statement
        init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Python Asteroid Shooter 3D")

        # Camera setup
        self.camera = Camera3D()
        # For the camera position, X-coordinate moves left/right, Y-coordinate moves up/down
        # and Z-coordinate moves forward/backwards
        self.camera.position = Vector3(-4.0, 8.0, 6.0)
        self.camera.target = Vector3(0.0, 0.0, -1.0)
        self.camera.up = Vector3(0.0, 1.0, 0.0)
        # Tells how the camera's field of view should be set up
        # The field of view is similar to zoom, although not exactly the same
        self.camera.fovy = 45.0
        self.camera.projection = CAMERA_PERSPECTIVE

        self.model_manager = ModelManager()

    def update(self):
        self.model_manager.update()

    def draw(self):
        clear_background(BACKGROUND_COLOR)
        begin_drawing()

        # We need "begin_mode_3d" and "end_mode_3d" to display 3D objects
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
