use bevy::{ecs::component::Component, math::Vec2};

use crate::plugins::BALL_STATIC_SPEED;

#[derive(Component)]
pub struct Ball {
    pub direction: Vec2,
    pub speed: f32,
}

impl Ball {
    pub fn new() -> Self {
        Ball {
            direction: Vec2::ZERO,
            speed: BALL_STATIC_SPEED,
        }
    }
}
