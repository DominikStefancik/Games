use bevy::prelude::Component;

#[derive(Component)]
pub struct Velocity {
    pub x: f32,
    pub y: f32,
}

// general component which represents anything that moves (player, enemies, lasers, etc.)
#[derive(Component)]
pub struct Movable {
    // used to detect if an object should be "destroyed" when it reaches the edge of the game window
    pub auto_despawn: bool,
}

#[derive(Component)]
pub struct Player;
