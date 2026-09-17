use bevy::ecs::resource::Resource;

use crate::plugins::{
    BOTTOM_OFFSET, INITIAL_LIVES_COUNT, INITIAL_MAX_LIVES_COUNT, LEVELS, MAX_LIVES_COUNT,
    PADDLE_INITIAL_SIZE, WINDOW_RESOLUTION_HALF,
};

#[derive(Resource)]
pub struct GameInfo {
    pub level: Level,
    pub lives: u16,
    pub max_lives: u16,
    pub score: u32,
}

impl GameInfo {
    pub fn init() -> Self {
        GameInfo {
            level: Level::init(),
            lives: INITIAL_LIVES_COUNT,
            max_lives: INITIAL_MAX_LIVES_COUNT,
            score: 0,
        }
    }

    pub fn reset(&mut self) {
        self.level.reset();
        self.lives = INITIAL_LIVES_COUNT;
        self.max_lives = INITIAL_MAX_LIVES_COUNT;
        self.score = 0;
    }

    pub fn move_to_next_level(&mut self) {
        self.level.move_to_next_level();

        if self.max_lives < MAX_LIVES_COUNT {
            self.max_lives += 1;
        }
    }

    pub fn is_last_level(&self) -> bool {
        self.level.current == self.level.last
    }
}

pub struct Level {
    current: usize,
    last: usize,
    pub map: &'static [&'static str],
}

impl Level {
    fn init() -> Self {
        Level {
            current: 1,
            last: LEVELS.len(),
            map: LEVELS[0],
        }
    }

    fn reset(&mut self) {
        self.current = 1;
        self.set_level_map();
    }

    fn move_to_next_level(&mut self) {
        self.current += 1;
        self.set_level_map();
    }

    fn set_level_map(&mut self) {
        self.map = LEVELS[self.current - 1];
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
            lower_border: -(WINDOW_RESOLUTION_HALF.y - BOTTOM_OFFSET) + PADDLE_INITIAL_SIZE.y / 2.,
        }
    }
}
