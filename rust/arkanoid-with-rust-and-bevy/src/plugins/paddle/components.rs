use bevy::{ecs::component::Component, math::Vec2};

use crate::plugins::{PADDLE_INITIAL_MOVEMENT_SPEED, PADDLE_INITIAL_SIZE};

#[derive(Component)]
pub struct Paddle {
    pub size: Vec2,
    pub direction: f32,
    pub speed: f32,
    pub laser_count: u8,
}

impl Paddle {
    pub fn reset(&mut self) {
        self.size = PADDLE_INITIAL_SIZE;
        self.direction = 0.;
        self.speed = PADDLE_INITIAL_MOVEMENT_SPEED;
        self.laser_count = 0;
    }
}
