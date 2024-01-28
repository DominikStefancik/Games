use bevy::prelude::{Color, Val, Vec2, Vec3};

pub const BACKGROUND_COLOR: Color = Color::rgb(0.9, 0.9, 0.9);

// Paddle constants
pub const PADDLE_START_Y: f32 = BOTTOM_WALL + 60.;
pub const PADDLE_SIZE: Vec2 = Vec2::new(120., 20.);
pub const PADDLE_WIDTH_HALF: f32 = PADDLE_SIZE.x / 2.;
pub const PADDLE_COLOR: Color = Color::rgb(0.3, 0.3, 0.7);
pub const PADDLE_SPEED: f32 = 500.;

// Ball constants
pub const BALL_STARTING_POSITION: Vec3 = Vec3::new(0., -50., 0.);
pub const BALL_INITIAL_DIRECTION: Vec2 = Vec2::new(0.5, -0.5);
pub const BALL_RADIUS: f32 = 15.;
pub const BALL_COLOR: Color = Color::rgb(1., 0.5, 0.5);
pub const BALL_SPEED: f32 = 400.;

// Wall constants
pub const LEFT_WALL: f32 = -450.;
pub const RIGHT_WALL: f32 = 450.;
pub const TOP_WALL: f32 = 300.;
pub const BOTTOM_WALL: f32 = -300.;
pub const WALL_THICKNESS: f32 = 10.;
pub const WALL_BLOCK_WIDTH: f32 = RIGHT_WALL - LEFT_WALL;
pub const WALL_BLOCK_HEIGHT: f32 = TOP_WALL - BOTTOM_WALL;
pub const WALL_COLOR: Color = Color::rgb(0.8, 0.8, 0.8);

// Brick constants
pub const BRICK_SIZE: Vec2 = Vec2::new(100., 30.);
pub const BRICK_COLOR: Color = Color::rgb(0.5, 0.5, 1.);
pub const GAP_BETWEEN_PADDLE_AND_BRICKS: f32 = 270.;
pub const GAP_BETWEEN_BRICKS: f32 = 5.;
pub const GAP_BETWEEN_BRICKS_AND_CEILING: f32 = 20.;
pub const GAP_BETWEEN_BRICKS_AND_SIDES: f32 = 20.;

// Scoreboard constants
pub const SCOREBOARD_FONT_SIZE: f32 = 40.;
pub const SCOREBOARD_TEXT_PADDING: Val = Val::Px(5.);
pub const SCOREBOARD_TEXT_COLOR: Color = Color::rgb(0.5, 0.5, 1.);
pub const SCOREBOARD_SCORE_COLOR: Color = Color::rgb(1., 0.5, 0.5);
