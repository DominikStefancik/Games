from settings import Camera3D, CAMERA_PERSPECTIVE, Vector3

# Camera setup
CAMERA = Camera3D()
CAMERA.position = Vector3(0.2, 16.0, -16.0)
CAMERA.target = Vector3(0.0, 0.0, -1.0)
CAMERA.up = Vector3(0.0, 1.0, 0.0)
CAMERA.fovy = 90.0
CAMERA.projection = CAMERA_PERSPECTIVE


def get_camera():
    return CAMERA
