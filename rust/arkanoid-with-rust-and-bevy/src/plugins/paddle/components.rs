use bevy::{ecs::component::Component, math::Vec2};

use crate::plugins::{INITIAL_PADDLE_SIZE, PADDLE_MOVEMENT_SPEED};

#[derive(Component)]
pub struct Paddle {
    pub size: Vec2,
    pub direction: f32,
    pub speed: f32,
    pub laser_count: u8,
}

impl Paddle {
    pub fn reset(&mut self) {
        self.size = INITIAL_PADDLE_SIZE;
        self.direction = 0.;
        self.speed = PADDLE_MOVEMENT_SPEED;
        self.laser_count = 0;
    }
}
