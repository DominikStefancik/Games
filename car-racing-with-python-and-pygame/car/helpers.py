import pygame

from constants import FINISH_LINE_POSITION
from helpers import render_text_center


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


def handle_cars_collision(
    surface, font, computer_car, player_car, border_mask, finish_line_mask, game_info
):
    if player_car.collide(border_mask) != None:
        player_car.bounce()

    computer_car_finish_line_collision_poi = computer_car.collide(
        finish_line_mask, *FINISH_LINE_POSITION
    )

    if computer_car_finish_line_collision_poi != None:
        render_text_center(surface, font, "You lost!")
        pygame.display.update()
        pygame.time.wait(5000)
        game_info.reset_game()
        computer_car.reset_position()
        player_car.reset_position()

    # The expression "*FINISH_LINE_POSITION" splits the tuple into two separate arguments
    # which are then passed to the method
    player_car_finish_line_collision_poi = player_car.collide(
        finish_line_mask, *FINISH_LINE_POSITION
    )

    if player_car_finish_line_collision_poi != None:
        # The point of intersection is a touple of X and Y values representing where the collision happened.
        # If the Y value is 0, that means the car collided with the finish line from the top.
        # However, we don't want to allow the player to cheat and cross the finish line from the top.
        # He has to go with his car all the way through the track and cross it from the bottom.
        if player_car_finish_line_collision_poi[1] == 0:
            player_car.bounce()
        else:
            game_info.next_level()
            computer_car.update_parameters(game_info.level)
            player_car.reset_position()
