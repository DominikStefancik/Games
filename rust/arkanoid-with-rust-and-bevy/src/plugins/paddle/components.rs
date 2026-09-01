use bevy::{ecs::component::Component, math::Vec2};

#[derive(Component)]
pub struct Paddle {
    pub size: Vec2,
    pub direction: f32,
    pub speed: f32,
    pub laser_count: u8,
}
