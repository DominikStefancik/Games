import pygame

def rotate_car_image_center(surface, image, top_left, angle):
    # The method "pygame.transform.rotate" will rotate the image around the top left hand corner
    rotated_image = pygame.transform.rotate(image, angle)

    # However, we want the image to be rotated around its center
    #
    # The image doesn't know its X and Y position, that's why we have to set the parameter "topleft"
    original_image_rectangle = image.get_rect(topleft=top_left)
    # We want to remove the offset so we rotate the image around its center
    # without changing its X and Y position
    new_rectangle = rotated_image.get_rect(center=original_image_rectangle.center)
    surface.blit(rotated_image, new_rectangle.topleft)


def move_player_car(player_car):
    pressed_keys = pygame.key.get_pressed()
    car_moved = False

    if pressed_keys[pygame.K_LEFT]:
        player_car.rotate(left=True)
    if pressed_keys[pygame.K_RIGHT]:
        player_car.rotate(right=True)
    if pressed_keys[pygame.K_UP]:
        car_moved = True
        player_car.move_forward()
    if pressed_keys[pygame.K_DOWN]:
        car_moved = True
        player_car.move_backward()

    # If we stopped pressing the "UP" key, the car should be slowing down
    if not car_moved:
        player_car.reduce_speed()
