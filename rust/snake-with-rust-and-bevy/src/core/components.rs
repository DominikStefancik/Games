use bevy::ecs::component::Component;

// Every object in Snake lives on a discrete grid cell
#[derive(Component, Clone, Copy, Debug)]
pub struct GridPosition {
    pub column: u32,
    pub row: u32,
}

impl GridPosition {
    pub fn new(column: u32, row: u32) -> Self {
        GridPosition { column, row }
    }
}
