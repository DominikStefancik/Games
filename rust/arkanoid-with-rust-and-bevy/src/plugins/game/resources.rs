use bevy::ecs::resource::Resource;

use crate::plugins::{BOTTOM_OFFSET, PADDLE_SIZE, WINDOW_RESOLUTION};

#[derive(Resource, Debug)]
pub struct MovingArea {
    pub left_border: f32,
    pub right_border: f32,
    pub upper_border: f32,
    pub lower_border: f32,
}

impl MovingArea {
    pub fn new() -> Self {
        let horizontal_border = (WINDOW_RESOLUTION.0 / 2) as f32;
        let vertical_border = (WINDOW_RESOLUTION.1 / 2) as f32;

        MovingArea {
            left_border: -horizontal_border,
            right_border: horizontal_border,
            upper_border: vertical_border,
            lower_border: -(vertical_border - BOTTOM_OFFSET) + PADDLE_SIZE.y / 2.,
        }
    }
}
