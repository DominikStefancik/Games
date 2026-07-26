use bevy::ecs::{
    resource::Resource,
    world::{FromWorld, World},
};

use crate::core::{Direction, Grid, GridPosition};

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

// When implementing this trait, we can then initialise a Resource on the App level
// by calling the ".init_resource::<Snake>()"
impl FromWorld for Snake {
    fn from_world(world: &mut World) -> Self {
        // in order to use the Grid, we have to add the SharedPlugin to the app before the SnakePlugin,
        // because the Grid is registered there
        let grid = world.resource::<Grid>();
        let start_column = grid.size.x / 2;
        let start_row = grid.size.y / 2;

        Snake::new(start_column, start_row)
    }
}
