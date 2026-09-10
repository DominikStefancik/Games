use bevy::ecs::resource::Resource;

use crate::plugins::{
    BOTTOM_OFFSET, INITIAL_LIVES_COUNT, INITIAL_MAX_LIVES_COUNT, INITIAL_PADDLE_SIZE,
    WINDOW_RESOLUTION_HALF, get_level_map,
};

#[derive(Resource)]
pub struct GameInfo {
    pub current_level: u8,
    pub level_count: u8,
    pub level_map: Vec<&'static str>,
    pub lives: u16,
    pub max_lives: u16,
    pub score: u32,
}

impl GameInfo {
    pub fn init() -> Self {
        GameInfo {
            current_level: 1,
            level_count: 2,
            level_map: get_level_map(1).unwrap(),
            lives: INITIAL_LIVES_COUNT,
            max_lives: INITIAL_MAX_LIVES_COUNT,
            score: 0,
        }
    }

    pub fn reset(&mut self) {
        self.current_level = 1;
        self.level_map = get_level_map(1).unwrap();
        self.lives = INITIAL_LIVES_COUNT;
        self.max_lives = INITIAL_MAX_LIVES_COUNT;
        self.score = 0;
    }

    pub fn move_to_next_level(&mut self) {
        self.current_level += 1;
        self.level_map = get_level_map(self.current_level).unwrap();
        self.max_lives += 1;
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
