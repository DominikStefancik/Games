use crate::position::Position;

pub const TOP_MARGIN: f32 = 60.;
pub const BOTTOM_MARGIN: f32 = 60.;
pub const LEFT_MARGIN: f32 = 80.;
pub const RIGHT_MARGIN: f32 = 80.;

pub const NEIGHBOURS_DIFFERENCE: &[Position<i32>] = &[
    Position::new(1, 1),
    Position::new(1, 0),
    Position::new(1, -1),
    Position::new(-1, 1),
    Position::new(-1, 0),
    Position::new(-1, -1),
    Position::new(0, 1),
    Position::new(0, -1),
];
