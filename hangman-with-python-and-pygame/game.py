import random

from constants import (
    BUTTON_GAP_SIZE,
    BUTTONS_IN_ROW,
    BUTTON_RADIUS,
    BUTTON_ROWS,
    LETTER_A_ASCII_CODE,
    WINDOW_WIDTH,
    WORDS,
)
from hangman_status import HangmanStatus


class Game:
    def __init__(self):
        self.hangman_status = HangmanStatus.EMPTY_ROPE
        self.word = random.choice(WORDS)
        self.guessed_letters = []

        # Each letter will be an array of items [character, x-position, y-position, is_visible]
        # We want to modify properties of these items and with using an array it is easier than using a tuple
        # (see setting up visibility after a player clicks on a letter)
        self.letters = []
        distance_between_two_buttons = BUTTON_RADIUS * 2 + BUTTON_GAP_SIZE
        button_start_position_x = round(
            (WINDOW_WIDTH - distance_between_two_buttons * BUTTONS_IN_ROW) / BUTTON_ROWS
        )
        button_start_position_y = 430
        for index in range(26):
            position_x = (
                button_start_position_x
                + BUTTON_GAP_SIZE * 2
                + distance_between_two_buttons * (index % BUTTONS_IN_ROW)
            )
            position_y = (
                button_start_position_y
                + (index // BUTTONS_IN_ROW) * distance_between_two_buttons
            )
            # The function "chr()" returns a character representation of the number we give it as a parameter
            self.letters.append(
                [chr(LETTER_A_ASCII_CODE + index), position_x, position_y, True]
            )

    def update_status(self):
        next_status = int(self.hangman_status) + 1
        self.hangman_status = HangmanStatus.from_int(next_status)

    def reset(self):
        self.word = random.choice(WORDS)
        self.guessed_letters = []
        self.hangman_status = HangmanStatus.EMPTY_ROPE

        for letter in self.letters:
            letter[3] = True
