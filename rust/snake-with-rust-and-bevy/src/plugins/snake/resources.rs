use bevy::ecs::resource::Resource;

use crate::core::{Direction, GridPosition};

#[derive(Resource)]
pub struct Snake {
    pub segments: Vec<GridPosition>,
    pub direction: Direction,
}

impl Snake {
    pub fn new(start_column: i32, start_row: i32) -> Self {
        Snake {
            segments: vec![
                GridPosition::new(start_column, start_row),
                GridPosition::new(start_column - 1, start_row),
                GridPosition::new(start_column - 2, start_row),
            ],
            direction: Direction::Right,
        }
    }

    pub fn restart(&mut self, start_column: i32, start_row: i32) {
        self.segments = vec![
            GridPosition::new(start_column, start_row),
            GridPosition::new(start_column - 1, start_row),
            GridPosition::new(start_column - 2, start_row),
        ];
        self.direction = Direction::Right;
    }
}
