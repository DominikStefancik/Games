use crate::position::Position;

pub const TOP_MARGIN: f32 = 60.;
pub const BOTTOM_MARGIN: f32 = 60.;
pub const LEFT_MARGIN: f32 = 140.;
pub const RIGHT_MARGIN: f32 = 80.;

pub const CONTROL_RECTANGLE_X: f32 = 20.;
pub const CONTROL_RECTANGLE_WIDTH: f32 = 100.;
pub const CONTROL_RECTANGLE_HEIGHT: f32 = 30.;
pub const CONTROL_RECTANGLE_BOTTOM_MARGIN: f32 = 15.;
pub const CONTROL_TEXT_LEFT_PADDING: f32 = 15.;
pub const CONTROL_TEXT_TOP_PADDING: f32 = 22.;
pub const CONTROL_TEXT_SIZE: f32 = 25.;

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
