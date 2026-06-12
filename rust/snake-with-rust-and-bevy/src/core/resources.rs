use bevy::{
    ecs::resource::Resource,
    math::{UVec2, Vec3},
};

use crate::core::{GRID_PIXELS, GRID_SIZE, GridPosition};

// If the data rarely changes during the game, it's better to use Resource rather than a Component
// From the perfomance point of view, Resources can render much faster then Components and can run in parallel
#[derive(Resource)]
pub struct GridSize {
    size: UVec2,
    pixels: u32,
}

impl GridSize {
    pub fn default() -> Self {
        return GridSize {
            size: UVec2::splat(GRID_SIZE),
            pixels: GRID_PIXELS,
        };
    }

    // translates grid position into a pixels position
    pub fn to_pixels(&self, position: GridPosition) -> Vec3 {
        let half_width = self.size.x as f32 * GRID_PIXELS as f32 / 2.0;
        let half_height = self.size.y as f32 * GRID_PIXELS as f32 / 2.0;

        Vec3::new(
            position.column as f32 * 0.5 + self.pixels as f32 / 2.0 - half_width,
            position.row as f32 * 0.5 + self.pixels as f32 / 2.0 - half_height,
            0.0,
        )
    }
}
