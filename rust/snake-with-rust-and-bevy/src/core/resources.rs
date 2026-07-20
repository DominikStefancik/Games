use bevy::{
    asset::Handle,
    ecs::resource::Resource,
    math::{UVec2, Vec3},
    text::Font,
};

use crate::core::{CELL_PIXELS, GRID_SIZE, GridPosition};

#[derive(Resource)]
pub struct GameFonts {
    pub bebas_neue_regular: Handle<Font>,
}

// If the data rarely changes during the game, it's better to use Resource rather than a Component
// From the perfomance point of view, Resources can render much faster then Components and can run in parallel
#[derive(Resource)]
pub struct GridSize {
    pub size: UVec2,
    pub pixels: u32,
}

impl GridSize {
    pub fn default() -> Self {
        GridSize {
            size: UVec2::splat(GRID_SIZE),
            pixels: CELL_PIXELS,
        }
    }

    // translates grid position into a pixels position
    pub fn to_pixels(&self, position: GridPosition, z_index: f32) -> Vec3 {
        let half_width = self.size.x as f32 * self.pixels as f32 / 2.0;
        let half_height = self.size.y as f32 * self.pixels as f32 / 2.0;

        Vec3::new(
            position.column as f32 * self.pixels as f32 + self.pixels as f32 / 2.0 - half_width,
            position.row as f32 * self.pixels as f32 + self.pixels as f32 / 2.0 - half_height,
            z_index,
        )
    }
}
