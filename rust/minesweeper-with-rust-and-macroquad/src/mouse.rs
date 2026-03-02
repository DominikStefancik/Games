use crate::position::Position;
use macroquad::input::{MouseButton, is_mouse_button_pressed, mouse_position};

pub fn get_pressed_mouse_position(button: MouseButton) -> Option<Position<f32>> {
    if is_mouse_button_pressed(button) {
        let (x, y) = mouse_position();
        return Some(Position::new(x, y));
    };

    None
}
