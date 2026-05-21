use std::time::Duration;

use bevy::{
    ecs::resource::Resource,
    prelude::{Deref, DerefMut},
    time::{Timer, TimerMode},
};
use rand::{RngExt, rng};

#[derive(Resource, Deref, DerefMut)]
pub struct MotobugGenerationTimer(pub Timer);

impl MotobugGenerationTimer {
    pub fn new(seconds: f32) -> Self {
        MotobugGenerationTimer(Timer::from_seconds(seconds, TimerMode::Repeating))
    }

    pub fn set_random(&mut self) {
        let value = rng().random_range(0.7..3.0);
        self.0.set_duration(Duration::from_secs_f32(value));
    }
}
