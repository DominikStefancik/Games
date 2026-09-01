use bevy::ecs::resource::Resource;

use crate::plugins::{BOTTOM_OFFSET, LEVEL_1_MAP, PADDLE_SIZE, WINDOW_RESOLUTION_HALF};

#[derive(Resource)]
pub struct GameInfo {
    pub current_level: u16,
    pub level_map: Vec<&'static str>,
    pub lives: u16,
}

impl GameInfo {
    pub fn init() -> Self {
        GameInfo {
            current_level: 1,
            level_map: LEVEL_1_MAP.to_vec(),
            lives: 3,
        }
    }
}

#[derive(Resource, Debug)]
pub struct MovingArea {
    pub left_border: f32,
    pub right_border: f32,
    pub upper_border: f32,
    pub lower_border: f32,
}

impl MovingArea {
    pub fn new() -> Self {
        MovingArea {
            left_border: -WINDOW_RESOLUTION_HALF.x,
            right_border: WINDOW_RESOLUTION_HALF.x,
            upper_border: WINDOW_RESOLUTION_HALF.y,
            lower_border: -(WINDOW_RESOLUTION_HALF.y - BOTTOM_OFFSET) + PADDLE_SIZE.y / 2.,
        }
    }
}
