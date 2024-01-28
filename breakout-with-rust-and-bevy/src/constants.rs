use bevy::prelude::{Color, Vec2, Vec3};

pub const BACKGROUND_COLOR: Color = Color::rgb(0.9, 0.9, 0.9);

pub const PADDLE_START_Y: f32 = 0.;
pub const PADDLE_SIZE: Vec2 = Vec2::new(120., 20.);
pub const PADDLE_COLOR: Color = Color::rgb(0.3, 0.3, 0.7);
pub const PADDLE_SPEED: f32 = 500.;

pub const BALL_STARTING_POSITION: Vec3 = Vec3::new(0., -50., 0.);
pub const BALL_INITIAL_DIRECTION: Vec2 = Vec2::new(0.5, -0.5);
pub const BALL_RADIUS: f32 = 15.;
pub const BALL_COLOR: Color = Color::rgb(1., 0.5, 0.5);
pub const BALL_SPEED: f32 = 400.;

pub const LEFT_WALL: f32 = -450.;
pub const RIGHT_WALL: f32 = 450.;
pub const TOP_WALL: f32 = 300.;
pub const BOTTOM_WALL: f32 = -300.;
pub const WALL_THICKNESS: f32 = 10.;
pub const WALL_BLOCK_WIDTH: f32 = RIGHT_WALL - LEFT_WALL;
pub const WALL_BLOCK_HEIGHT: f32 = TOP_WALL - BOTTOM_WALL;
pub const WALL_COLOR: Color = Color::rgb(0.8, 0.8, 0.8);
