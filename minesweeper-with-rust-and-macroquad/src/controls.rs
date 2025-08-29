use crate::constants::{
    CONTROL_RECTANGLE_BOTTOM_MARGIN, CONTROL_RECTANGLE_HEIGHT, CONTROL_RECTANGLE_WIDTH,
    CONTROL_RECTANGLE_X, CONTROL_TEXT_LEFT_PADDING, CONTROL_TEXT_SIZE, CONTROL_TEXT_TOP_PADDING,
    TOP_MARGIN,
};
use crate::mouse::get_pressed_mouse_position;
use crate::position::Position;
use macroquad::color::{BLACK, Color, GREEN, ORANGE, RED};
use macroquad::input::MouseButton;
use macroquad::prelude::draw_text;
use macroquad::shapes::draw_rectangle;

enum RectangleType {
    Small,
    Medium,
    Large,
}

struct Rectangle {
    x: f32,
    y: f32,
    width: f32,
    height: f32,
    color: Color,
    rectangle_type: RectangleType,
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
                x: CONTROL_RECTANGLE_X,
                y: TOP_MARGIN,
                width: CONTROL_RECTANGLE_WIDTH,
                height: CONTROL_RECTANGLE_HEIGHT,
                color: GREEN,
                rectangle_type: RectangleType::Small,
            },
            medium: Rectangle {
                x: CONTROL_RECTANGLE_X,
                y: TOP_MARGIN + CONTROL_RECTANGLE_HEIGHT + CONTROL_RECTANGLE_BOTTOM_MARGIN,
                width: CONTROL_RECTANGLE_WIDTH,
                height: CONTROL_RECTANGLE_HEIGHT,
                color: ORANGE,
                rectangle_type: RectangleType::Medium,
            },
            large: Rectangle {
                x: CONTROL_RECTANGLE_X,
                y: TOP_MARGIN + (CONTROL_RECTANGLE_HEIGHT + CONTROL_RECTANGLE_BOTTOM_MARGIN) * 2.,
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
            CONTROL_TEXT_SIZE,
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
            CONTROL_TEXT_SIZE,
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
            CONTROL_TEXT_SIZE,
            BLACK,
        );
    }

    pub fn handle_mouse_click(&self) {
        if let Some(position) = get_pressed_mouse_position(MouseButton::Left) {
            // first find out which control was clicked on via a cursor position
            let position = match self.resolve_rectangle_position(&position) {
                Some(position) => position,
                None => return,
            };
        }
    }

    fn resolve_rectangle_position(&self, position: &Position<f32>) -> Option<Position<f32>> {
        None
    }
}
