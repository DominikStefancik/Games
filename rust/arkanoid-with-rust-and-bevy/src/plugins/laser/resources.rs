use bevy::{ecs::resource::Resource, time::Timer};

#[derive(Resource)]
pub struct LaserCooldownTimer(pub Timer);
