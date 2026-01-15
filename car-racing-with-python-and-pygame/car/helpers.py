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
