use bevy::{
    ecs::{component::Component, entity::Entity},
    math::Vec2,
};

#[derive(Component)]
pub struct Collider {
    pub size: Vec2,
}

#[derive(Component)]
pub struct BoxTextureParts {
    pub top_left: Entity,
    pub top: Entity,
    pub top_right: Entity,
    pub left: Entity,
    pub right: Entity,
    pub bottom_left: Entity,
    pub bottom: Entity,
    pub bottom_right: Entity,
    pub center: Entity,
}
