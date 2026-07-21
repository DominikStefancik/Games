use bevy::ecs::resource::Resource;

use crate::core::GridPosition;

#[derive(Clone, Copy, PartialEq, Eq, Debug)]
pub enum Direction {
    Up,
    Down,
    Left,
    Right,
}

#[derive(Resource)]
pub struct Snake {
    pub segments: Vec<GridPosition>,
    pub direction: Direction,
}

impl Snake {
    pub fn new(start_column: u32, start_row: u32) -> Self {
        Snake {
            segments: vec![
                GridPosition::new(start_column, start_row),
                GridPosition::new(start_column - 1, start_row),
                GridPosition::new(start_column - 2, start_row),
            ],
            direction: Direction::Right,
        }
    }

    pub fn restart(&mut self, start_column: u32, start_row: u32) {
        self.segments = vec![
            GridPosition::new(start_column, start_row),
            GridPosition::new(start_column - 1, start_row),
            GridPosition::new(start_column - 2, start_row),
        ];
        self.direction = Direction::Right;
    }
}
