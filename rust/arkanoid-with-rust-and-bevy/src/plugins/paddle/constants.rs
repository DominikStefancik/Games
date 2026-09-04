use bevy::math::Vec2;

pub const INITIAL_PADDLE_SIZE: Vec2 = Vec2::new(125., 35.);
pub const PADDLE_LENGTH_INCREASE: f32 = 10.;
pub const PADDLE_MOVEMENT_SPEED: f32 = 10.;

pub const LASER_TEXTURE_SIZE: Vec2 = Vec2::new(20., 28.);
pub const LASER_VERTICAL_OFFSET: f32 = 5.;
pub const LASER_GAP: f32 = 6.;
pub const LASER_MAX_COUNT: u8 = 5;
pub const PROJECTILE_TEXTURE_SIZE: Vec2 = Vec2::new(12., 40.);
pub const PROJECTILE_MOVEMENT_SPEED: f32 = 10.;
