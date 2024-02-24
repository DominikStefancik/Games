use bevy::prelude::Vec2;

pub const ARENA_WIDTH: f32 = 500.;
pub const ARENA_HEIGHT: f32 = 500.;

pub const PLAYER_WIDTH: f32 = 22.;
pub const PLAYER_HEIGHT: f32 = 32.;

pub const SPRITE_SHEET_SIZE: Vec2 = Vec2::new(58., 34.);
pub const LEFT_CAT_CORNER: Vec2 = Vec2::new(11., 1.);
pub const RIGHT_CAT_CORNER: Vec2 = Vec2::new(35., 1.);
pub const CAT_SIZE: Vec2 = Vec2::new(PLAYER_WIDTH, PLAYER_HEIGHT);
