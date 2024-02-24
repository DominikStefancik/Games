use bevy::prelude::Vec2;

pub const ARENA_WIDTH: f32 = 500.;
pub const ARENA_HEIGHT: f32 = 500.;

pub const PLAYER_WIDTH: f32 = 22.;
pub const PLAYER_HEIGHT: f32 = 32.;
pub const PLAYER_SPEED: f32 = 60.;

pub const BALL_VELOCITY: Vec2 = Vec2::new(30., 0.);
pub const BALL_RADIUS: f32 = 4.;

pub const SPRITES_SHEET_PATH: &str = "textures/spritesheet.png";
pub const SPRITES_SHEET_SIZE: Vec2 = Vec2::new(58., 34.);
pub const LEFT_CAT_TEXTURE_CORNER: Vec2 = Vec2::new(11., 1.);
pub const RIGHT_CAT_TEXTURE_CORNER: Vec2 = Vec2::new(35., 1.);
pub const CAT_SIZE: Vec2 = Vec2::new(PLAYER_WIDTH, PLAYER_HEIGHT);
pub const BALL_TEXTURE_CORNER: Vec2 = Vec2::new(1., 1.);
pub const BALL_SIZE: Vec2 = Vec2::new(8., 8.);

pub const GRAVITY_ACCELERATION: f32 = -40.;
