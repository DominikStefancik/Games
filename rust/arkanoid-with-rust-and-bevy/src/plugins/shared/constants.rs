use bevy::math::Vec2;

pub const CORNER_BOX_TEXTURE_SIZE: Vec2 = Vec2::new(14., 14.);

#[derive(Debug, PartialEq, Eq, Clone, Copy)]
pub enum CollisionSide {
    Left,
    Right,
    Top,
    Bottom,
}
