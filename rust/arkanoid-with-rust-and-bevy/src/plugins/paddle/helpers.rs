use bevy::math::Vec3;

use crate::plugins::{BOTTOM_OFFSET, WINDOW_RESOLUTION_HALF};

pub fn get_paddle_initial_position() -> Vec3 {
    Vec3::new(0., -WINDOW_RESOLUTION_HALF.y + BOTTOM_OFFSET, 1.)
}
