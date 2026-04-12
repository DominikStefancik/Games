import pygame


# This class is responsible for handling all inputs, by it via a keyboard or a mouse.
# It uses the "for event in pygame.event.get()" mechanism for detecting input events
# and sets flags representing that certain inputs were processed. Then this class is used as a singleton
# in the codebase where the input has to be checked.
#
# NOTE: The input is handled via InputManager using the "pygame.event.get()" queue and not calling methods like
# "pygame.key.get_pressed()" or "pygame.mouse.get_just_pressed()" in different places directly,
# because when creating a build package for running the game in a web browser (e.g. via Pygbag package),
# the methods like "pygame.key.get_pressed()" or "pygame.mouse.get_just_pressed()" don't work in the browser
# and input is not detected during the game.
# When using the "pygame.event.get()" queue approach, the input is detected whether the game runs locally
# on a computer or in a web browser.
class InputManager:
    def __init__(self):
        self._left_mouse_clicked = False
        self._exit_button_clicked = False

    @property
    def left_mouse_clicked(self):
        return self._left_mouse_clicked

    @property
    def exit_button_clicked(self):
        return self._exit_button_clicked

    def update(self):
        self._left_mouse_clicked = False
        self._exit_button_clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._exit_button_clicked = True

            # Handle mouse click event
            # "event.button == 1" represents the left mouse button
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._left_mouse_clicked = True


INPUT_MANAGER = InputManager()


def get_input_manager():
    return INPUT_MANAGER
