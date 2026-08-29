use bevy::{ecs::component::Component, math::Vec2};

#[derive(Component)]
pub struct Collider {
    pub size: Vec2,
}
