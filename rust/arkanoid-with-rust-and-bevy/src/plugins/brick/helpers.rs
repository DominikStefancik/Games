use bevy::math::{Vec2, Vec3};

use crate::plugins::{
    BRICK_HEIGHT, BRICK_SIDE_OFFSET, BRICK_TOP_OFFSET, BRICKS_GAP, WINDOW_RESOLUTION,
};

pub fn calculate_brick_size(bricks_in_row_count: f32) -> Vec2 {
    let brick_width = (WINDOW_RESOLUTION.0 as f32
        - BRICK_SIDE_OFFSET * 2.
        - (bricks_in_row_count - 1.) * BRICKS_GAP)
        / bricks_in_row_count;

    Vec2::new(brick_width, BRICK_HEIGHT)
}

pub fn calculate_brick_position(row_index: usize, brick_index: usize, brick_size: Vec2) -> Vec3 {
    let x_position =
        BRICK_SIDE_OFFSET + brick_index as f32 * (brick_size.x + BRICKS_GAP) + brick_size.x / 2.;

    let y_position =
        BRICK_TOP_OFFSET + row_index as f32 * (brick_size.y + BRICKS_GAP) + brick_size.y / 2.;

    Vec3::new(
        x_position - (WINDOW_RESOLUTION.0 / 2) as f32,
        (WINDOW_RESOLUTION.1 / 2) as f32 - y_position,
        1.,
    )
}
