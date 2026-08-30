use bevy::ecs::component::Component;

use crate::plugins::BrickType;

#[derive(Component)]
pub struct Brick {
    pub brick_type: BrickType,
}
