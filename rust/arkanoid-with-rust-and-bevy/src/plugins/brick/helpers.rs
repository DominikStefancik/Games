use bevy::math::{Vec2, Vec3};

use crate::plugins::{BRICK_HEIGHT, BRICKS_GAP, SIDE_OFFSET, TOP_OFFSET, WINDOW_RESOLUTION};

pub fn calculate_brick_size(bricks_in_row_count: u32) -> Vec2 {
    let brick_width =
        ((WINDOW_RESOLUTION.0 - SIDE_OFFSET * 2 - (bricks_in_row_count - 1) * BRICKS_GAP)
            / (bricks_in_row_count)) as f32;

    Vec2::new(brick_width, BRICK_HEIGHT)
}

pub fn calculate_brick_position(
    row_index: usize,
    character_index: usize,
    brick_size: Vec2,
) -> Vec3 {
    let x_position = SIDE_OFFSET as f32
        + character_index as f32 * (brick_size.x + BRICKS_GAP as f32)
        + brick_size.x / 2.;

    let y_position = TOP_OFFSET as f32
        + row_index as f32 * (brick_size.y + BRICKS_GAP as f32)
        + brick_size.y / 2.;

    Vec3::new(
        x_position - (WINDOW_RESOLUTION.0 / 2) as f32,
        (WINDOW_RESOLUTION.1 / 2) as f32 - y_position,
        1.,
    )
}
