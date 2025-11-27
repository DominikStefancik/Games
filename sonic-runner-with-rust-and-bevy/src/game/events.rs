use bevy::ecs::{entity::Entity, event::EntityEvent};

#[derive(EntityEvent)]
pub struct ScoreUpdated(pub Entity);
