use bevy::{color::Color, input::keyboard::KeyCode};

pub const WINDOW_RESOLUTION: (u32, u32) = (1400, 900);
pub const BACKGROUND_COLOR: Color = Color::srgb(13. / 255.0, 13. / 255., 24. / 255.);
pub const CANVAS_COLOR: Color = Color::srgb(31. / 255.0, 31. / 255., 45. / 255.);
pub const DEFAULT_TEXT_COLOR: Color = Color::srgb(200. / 255.0, 200. / 255., 200. / 255.);
pub const SNAKE_HEAD_COLOR: Color = Color::srgb(0.2, 0.95, 0.2);
pub const SNAKE_BODY_COLOR: Color = Color::srgb(0.2, 0.7, 0.2);
pub const FOOD_COLOR: Color = Color::srgb(0.8, 0.2, 0.2);

pub const INSTRUCTIONS_FONT_SIZE: f32 = 24.;

pub const GRID_SIZE: u32 = 20;
pub const CELL_PIXELS: u32 = 30; // number of pixels for each cell
pub const CELL_PADDING: u32 = 2;

pub const SNAKE_MOVE_INTERVAL: f32 = 0.15;

#[derive(Clone, Copy, PartialEq, Eq, Debug)]
pub enum Direction {
    Up,
    Down,
    Left,
    Right,
}

impl Direction {
    pub fn from_key(key_code: &KeyCode) -> Option<Self> {
        match key_code {
            KeyCode::ArrowLeft => Some(Direction::Left),
            KeyCode::ArrowRight => Some(Direction::Right),
            KeyCode::ArrowUp => Some(Direction::Up),
            KeyCode::ArrowDown => Some(Direction::Down),
            _ => None,
        }
    }

    pub fn is_opposite(&self, other: &Direction) -> bool {
        // matches! is a Rust macro that checks if a value matches a pattern
        matches!(
            (*self, *other),
            (Direction::Left, Direction::Right)
                | (Direction::Right, Direction::Left)
                | (Direction::Up, Direction::Down)
                | (Direction::Down, Direction::Up)
        )
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn from_key_matches_arrow_keys() {
        assert!(matches!(
            Direction::from_key(&KeyCode::ArrowLeft),
            Some(Direction::Left)
        ));

        assert!(matches!(
            Direction::from_key(&KeyCode::ArrowRight),
            Some(Direction::Right)
        ));

        assert!(matches!(
            Direction::from_key(&KeyCode::ArrowUp),
            Some(Direction::Up)
        ));

        assert!(matches!(
            Direction::from_key(&KeyCode::ArrowDown),
            Some(Direction::Down)
        ));
    }

    #[test]
    fn from_key_ignores_non_arrow_keys() {
        assert!(matches!(Direction::from_key(&KeyCode::Space), None));
        assert!(matches!(Direction::from_key(&KeyCode::KeyA), None));
    }

    #[test]
    fn directions_opposite_detected() {
        assert!(Direction::Left.is_opposite(&Direction::Right));
        assert!(Direction::Right.is_opposite(&Direction::Left));
        assert!(Direction::Up.is_opposite(&Direction::Down));
        assert!(Direction::Down.is_opposite(&Direction::Up));
    }

    #[test]
    fn directions_non_opposite_detected() {
        assert!(!Direction::Up.is_opposite(&Direction::Right));
        assert!(!Direction::Right.is_opposite(&Direction::Up));
        assert!(!Direction::Left.is_opposite(&Direction::Down));
        assert!(!Direction::Down.is_opposite(&Direction::Left));
    }
}
