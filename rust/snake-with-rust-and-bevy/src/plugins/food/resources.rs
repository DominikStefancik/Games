use bevy::ecs::resource::Resource;

use crate::core::GridPosition;

#[derive(Resource)]
pub struct Food(pub GridPosition);

impl Food {
    pub fn new(column: u32, row: u32) -> Self {
        Food(GridPosition::new(column, row))
    }
}
