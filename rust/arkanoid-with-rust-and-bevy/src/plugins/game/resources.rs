use bevy::ecs::resource::Resource;

use crate::plugins::{BOTTOM_OFFSET, INITIAL_PADDLE_SIZE, LEVEL_1_MAP, WINDOW_RESOLUTION_HALF};

#[derive(Resource)]
pub struct GameInfo {
    pub current_level: u16,
    pub level_map: Vec<&'static str>,
    pub lives: u16,
    pub score: u32,
}

impl GameInfo {
    pub fn init() -> Self {
        GameInfo {
            current_level: 1,
            level_map: LEVEL_1_MAP.to_vec(),
            lives: 3,
            score: 0,
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
            lower_border: -(WINDOW_RESOLUTION_HALF.y - BOTTOM_OFFSET) + INITIAL_PADDLE_SIZE.y / 2.,
        }
    }
}
