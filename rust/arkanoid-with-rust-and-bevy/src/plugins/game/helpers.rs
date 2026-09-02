use crate::plugins::{HEART_SIDE_OFFSET, HEART_TEXTURE_SIZE, HEARTS_GAP, WINDOW_RESOLUTION_HALF};

pub fn calculate_heart_horizontal_position(index: u16) -> f32 {
    WINDOW_RESOLUTION_HALF.x
        - HEART_SIDE_OFFSET
        - index as f32 * (HEART_TEXTURE_SIZE.x + HEARTS_GAP)
        - HEART_TEXTURE_SIZE.x / 2.
}
