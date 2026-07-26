use bevy::{ecs::component::Component, time::Timer};

#[derive(Component, Debug)]
pub struct GameStartingText(pub Timer);
