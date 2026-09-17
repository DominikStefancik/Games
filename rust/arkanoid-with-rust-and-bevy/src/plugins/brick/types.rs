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

impl From<char> for BrickType {
    fn from(letter: char) -> Self {
        match letter {
            '1' => BrickType::Blue,
            '2' => BrickType::Green,
            '3' => BrickType::Red,
            '4' => BrickType::Orange,
            '5' => BrickType::Purple,
            '6' => BrickType::Bronze,
            '7' => BrickType::Grey,
            _ => BrickType::Blue,
        }
    }
}
