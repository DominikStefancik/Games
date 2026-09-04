use bevy::math::Vec3;

use crate::plugins::{BOTTOM_OFFSET, LASER_GAP, LASER_TEXTURE_SIZE, WINDOW_RESOLUTION_HALF};

pub fn get_paddle_initial_position() -> Vec3 {
    Vec3::new(0., -WINDOW_RESOLUTION_HALF.y + BOTTOM_OFFSET, 1.)
}

pub fn get_laser_horizontal_position(half_paddle_size: f32, laser_count: u8, index: usize) -> f32 {
    match laser_count {
        1 => 0.,
        2 => {
            if index == 0 {
                -half_paddle_size / 2.
            } else {
                half_paddle_size / 2.
            }
        }
        3 => {
            if index == 0 {
                -half_paddle_size / 2.
            } else if index == 1 {
                0.
            } else {
                half_paddle_size / 2.
            }
        }
        4 => {
            if index == 0 {
                -half_paddle_size + LASER_TEXTURE_SIZE.x
            } else if index == 1 {
                -half_paddle_size + LASER_TEXTURE_SIZE.x * 2. + LASER_GAP
            } else if index == 2 {
                half_paddle_size - LASER_TEXTURE_SIZE.x * 2. - LASER_GAP
            } else {
                half_paddle_size - LASER_TEXTURE_SIZE.x
            }
        }
        5 => {
            if index == 0 {
                -half_paddle_size + LASER_TEXTURE_SIZE.x
            } else if index == 1 {
                -half_paddle_size + LASER_TEXTURE_SIZE.x * 2.
            } else if index == 2 {
                0.
            } else if index == 3 {
                half_paddle_size - LASER_TEXTURE_SIZE.x * 2.
            } else {
                half_paddle_size - LASER_TEXTURE_SIZE.x
            }
        }
        _ => 0.,
    }
}
