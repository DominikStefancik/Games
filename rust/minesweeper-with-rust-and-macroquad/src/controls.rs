use crate::constants::{
    BOARD_TOP_MARGIN, CONTROL_RECTANGLE_BOTTOM_MARGIN, CONTROL_RECTANGLE_HEIGHT,
    CONTROL_RECTANGLE_MARGIN, CONTROL_RECTANGLE_WIDTH, CONTROL_TEXT_LEFT_PADDING,
    CONTROL_TEXT_TOP_PADDING, END_TEXT_LEFT_PADDING, END_TEXT_TOP_PADDING, TEXT_SIZE,
};
use crate::minesweeper::GameState;
use crate::mouse::get_pressed_mouse_position;
use crate::position::Position;
use macroquad::color::{BLACK, Color, GREEN, ORANGE, RED};
use macroquad::input::MouseButton;
use macroquad::prelude::draw_text;
use macroquad::shapes::draw_rectangle;

#[derive(Copy, Clone, PartialEq)]
pub enum RectangleType {
    Small,
    Medium,
    Large,
}

#[derive(Copy, Clone)]
pub struct Rectangle {
    x: f32,
    y: f32,
    width: f32,
    height: f32,
    color: Color,
    pub rectangle_type: RectangleType,
}

pub struct Controls {
    small: Rectangle,
    medium: Rectangle,
    large: Rectangle,
}

impl Controls {
    pub fn new() -> Self {
        Controls {
            small: Rectangle {
                x: CONTROL_RECTANGLE_MARGIN,
                y: BOARD_TOP_MARGIN,
                width: CONTROL_RECTANGLE_WIDTH,
                height: CONTROL_RECTANGLE_HEIGHT,
                color: GREEN,
                rectangle_type: RectangleType::Small,
            },
            medium: Rectangle {
                x: CONTROL_RECTANGLE_MARGIN,
                y: BOARD_TOP_MARGIN + CONTROL_RECTANGLE_HEIGHT + CONTROL_RECTANGLE_BOTTOM_MARGIN,
                width: CONTROL_RECTANGLE_WIDTH,
                height: CONTROL_RECTANGLE_HEIGHT,
                color: ORANGE,
                rectangle_type: RectangleType::Medium,
            },
            large: Rectangle {
                x: CONTROL_RECTANGLE_MARGIN,
                y: BOARD_TOP_MARGIN
                    + (CONTROL_RECTANGLE_HEIGHT + CONTROL_RECTANGLE_BOTTOM_MARGIN) * 2.,
                width: CONTROL_RECTANGLE_WIDTH,
                height: CONTROL_RECTANGLE_HEIGHT,
                color: RED,
                rectangle_type: RectangleType::Large,
            },
        }
    }

    pub fn draw(&self) {
        draw_rectangle(
            self.small.x,
            self.small.y,
            self.small.width,
            self.small.height,
            self.small.color,
        );
        draw_text(
            "SMALL",
            self.small.x + CONTROL_TEXT_LEFT_PADDING,
            self.small.y + CONTROL_TEXT_TOP_PADDING,
            TEXT_SIZE,
            BLACK,
        );

        draw_rectangle(
            self.medium.x,
            self.medium.y,
            self.medium.width,
            self.medium.height,
            self.medium.color,
        );
        draw_text(
            "MEDIUM",
            self.medium.x + CONTROL_TEXT_LEFT_PADDING,
            self.medium.y + CONTROL_TEXT_TOP_PADDING,
            TEXT_SIZE,
            BLACK,
        );

        draw_rectangle(
            self.large.x,
            self.large.y,
            self.large.width,
            self.large.height,
            self.large.color,
        );
        draw_text(
            "LARGE",
            self.large.x + CONTROL_TEXT_LEFT_PADDING,
            self.large.y + CONTROL_TEXT_TOP_PADDING,
            TEXT_SIZE,
            BLACK,
        );
    }

    pub fn handle_mouse_click(&self) -> Option<Rectangle> {
        if let Some(position) = get_pressed_mouse_position(MouseButton::Left) {
            return self.resolve_rectangle_position(&position);
        }

        None
    }

    fn resolve_rectangle_position(&self, position: &Position<f32>) -> Option<Rectangle> {
        // this condition will not change
        let is_within_rectangle_width = CONTROL_RECTANGLE_MARGIN <= position.x
            && position.x <= CONTROL_RECTANGLE_MARGIN + CONTROL_RECTANGLE_WIDTH;
        // for the y-coordinate we need to check each rectangle separately
        let is_within_rectangle_height =
            self.small.y <= position.y && position.y <= self.small.y + CONTROL_RECTANGLE_HEIGHT;

        if is_within_rectangle_width && is_within_rectangle_height {
            return Some(self.small);
        }

        let is_within_rectangle_height =
            self.medium.y <= position.y && position.y <= self.medium.y + CONTROL_RECTANGLE_HEIGHT;

        if is_within_rectangle_width && is_within_rectangle_height {
            return Some(self.medium);
        }

        let is_within_rectangle_height =
            self.large.y <= position.y && position.y <= self.large.y + CONTROL_RECTANGLE_HEIGHT;

        if is_within_rectangle_width && is_within_rectangle_height {
            return Some(self.large);
        }

        None
    }

    pub fn show_finishing_text(&self, game_state: &GameState) {
        match game_state {
            GameState::Playing => {}
            GameState::Won => {
                draw_text(
                    "You won!",
                    self.large.x + END_TEXT_LEFT_PADDING,
                    self.large.y + END_TEXT_TOP_PADDING,
                    TEXT_SIZE,
                    BLACK,
                );
            }
            GameState::Lost => {
                draw_text(
                    "You lost!",
                    self.large.x + END_TEXT_LEFT_PADDING,
                    self.large.y + END_TEXT_TOP_PADDING,
                    TEXT_SIZE,
                    BLACK,
                );
            }
        }
    }
}
