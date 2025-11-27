use std::time::Duration;

use bevy::{
    ecs::resource::Resource,
    prelude::{Deref, DerefMut},
    time::{Timer, TimerMode},
};
use rand::{Rng, rng};

#[derive(Resource, Deref, DerefMut)]
pub struct RingGenerationTimer(pub Timer);

impl RingGenerationTimer {
    pub fn new(seconds: f32) -> Self {
        RingGenerationTimer(Timer::from_seconds(seconds, TimerMode::Repeating))
    }

    pub fn set_random(&mut self) {
        let value = rng().random_range(0.5..2.5);
        self.0.set_duration(Duration::from_secs_f32(value));
    }
}
