use crate::plugins::WINDOW_RESOLUTION;

pub const BRICK_HEIGHT: f32 = (WINDOW_RESOLUTION.1 / 15) as f32;

#[derive(Clone, Copy, PartialEq, Eq)]
pub enum BrickType {
    Blue,
    Green,
    Red,
    Orange,
    Purple,
    Bronze,
    Grey,
}

impl From<&str> for BrickType {
    fn from(letter: &str) -> Self {
        match letter {
            "1" => BrickType::Blue,
            "2" => BrickType::Green,
            "3" => BrickType::Red,
            "4" => BrickType::Orange,
            "5" => BrickType::Purple,
            "6" => BrickType::Bronze,
            "7" => BrickType::Grey,
            _ => BrickType::Blue,
        }
    }
}
