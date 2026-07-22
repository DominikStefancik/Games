use bevy::ecs::component::Component;

// Every object in Snake lives on a discrete grid cell
#[derive(Component, Clone, Copy, Debug, PartialEq, Eq)]
pub struct GridPosition {
    pub column: i32,
    pub row: i32,
}

impl GridPosition {
    pub fn new(column: i32, row: i32) -> Self {
        GridPosition { column, row }
    }
}
