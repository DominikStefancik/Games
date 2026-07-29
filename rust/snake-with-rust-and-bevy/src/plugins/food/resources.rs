use bevy::ecs::{
    resource::Resource,
    world::{FromWorld, World},
};

use crate::plugins::shared::{Grid, GridPosition};

#[derive(Resource)]
pub struct Food(pub GridPosition);

impl Food {
    pub fn new(column: i32, row: i32) -> Self {
        Food(GridPosition::new(column, row))
    }
}

// When implementing this trait, we can then initialise a Resource on the App level
// by calling the ".init_resource::<Food>()"
impl FromWorld for Food {
    fn from_world(world: &mut World) -> Self {
        // in order to use the Grid, we have to add the SharedPlugin to the app before the FoodPlugin,
        // because the Grid is registered there
        let grid = world.resource::<Grid>();

        let start_column = grid.size.x / 2;
        let start_row = grid.size.y / 2;

        Food::new(start_column, start_row)
    }
}
