use bevy::{ecs::component::Component, math::Vec2, time::Timer};

#[derive(Component, Debug)]
pub struct FoodSprite;

#[derive(Component, Debug)]
pub struct FoodParticle {
    pub velocity: Vec2,
    pub timer: Timer,
}
