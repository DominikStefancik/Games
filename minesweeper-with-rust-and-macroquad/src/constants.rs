use crate::position::Position;

pub const BOARD_TOP_MARGIN: f32 = 60.;
pub const BOARD_BOTTOM_MARGIN: f32 = 60.;
pub const BOARD_LEFT_MARGIN: f32 = 140.;
pub const BOARD_RIGHT_MARGIN: f32 = 80.;

pub const CONTROL_RECTANGLE_MARGIN: f32 = 20.;
pub const CONTROL_RECTANGLE_WIDTH: f32 = 100.;
pub const CONTROL_RECTANGLE_HEIGHT: f32 = 30.;
pub const CONTROL_RECTANGLE_BOTTOM_MARGIN: f32 = 15.;
pub const CONTROL_TEXT_LEFT_PADDING: f32 = 15.;
pub const CONTROL_TEXT_TOP_PADDING: f32 = 22.;
pub const END_TEXT_LEFT_PADDING: f32 = 5.;
pub const END_TEXT_TOP_PADDING: f32 = 70.;
pub const TEXT_SIZE: f32 = 25.;

pub const NEIGHBOURS_DIFFERENCES: &[Position<i32>] = &[
    Position::new(1, 1),
    Position::new(1, 0),
    Position::new(1, -1),
    Position::new(-1, 1),
    Position::new(-1, 0),
    Position::new(-1, -1),
    Position::new(0, 1),
    Position::new(0, -1),
];
