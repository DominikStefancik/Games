use crate::plugins::PADDLE_MOVEMENT_SPEED;

pub const BALL_RADIUS: f32 = 16.;
pub const BALL_STATIC_SPEED: f32 = PADDLE_MOVEMENT_SPEED;
pub const BALL_MOVEMENT_SPEED: f32 = PADDLE_MOVEMENT_SPEED - 4.;

#[derive(Debug, PartialEq, Eq, Clone, Copy)]
pub enum CollisionSide {
    Left,
    Right,
    Top,
    Bottom,
}
