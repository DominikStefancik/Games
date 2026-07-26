use bevy::math::Vec3;

use crate::core::{Grid, GridPosition};

pub fn get_score_text_right_offset(grid: &Grid, y_offset: f32, z_index: f32) -> Vec3 {
    grid.to_pixels(GridPosition::new(grid.size.x, grid.size.y / 2), z_index)
        + Vec3::new(110., y_offset, 0.)
}
