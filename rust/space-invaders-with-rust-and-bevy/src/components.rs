use bevy::prelude::{Component, Timer, TimerMode, Vec2, Vec3};

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
pub struct Laser;

#[derive(Component)]
pub struct SpriteSize(pub Vec2);

impl From<(f32, f32)> for SpriteSize {
    fn from(value: (f32, f32)) -> Self {
        SpriteSize(Vec2::new(value.0, value.1))
    }
}

#[derive(Component)]
pub struct Player;

#[derive(Component)]
pub struct LaserFromPlayer;

#[derive(Component)]
pub struct Enemy;

#[derive(Component)]
pub struct LaserFromEnemy;

#[derive(Component)]
pub struct Explosion;

// Represents data about the explosion which is going to be spawned
// the argument represents a position where the explosion needs to be spawned
#[derive(Component)]
pub struct ExplosionToSpawn(pub Vec3);

#[derive(Component)]
pub struct ExplosionTimer(pub Timer);

impl Default for ExplosionTimer {
    fn default() -> Self {
        // the timer will be reset every 50 milliseconds
        Self(Timer::from_seconds(0.05, TimerMode::Repeating))
    }
}
