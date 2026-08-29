use bevy::{
    ecs::system::{Res, Single},
    input::{ButtonInput, keyboard::KeyCode},
};

use crate::plugins::Paddle;

pub fn update_paddle_direction_on_keypress(
    keyboard_input: Res<ButtonInput<KeyCode>>,
    mut paddle: Single<&mut Paddle>,
) {
    if keyboard_input.just_pressed(KeyCode::ArrowLeft) {
        paddle.direction = -1.;
    }

    if keyboard_input.just_pressed(KeyCode::ArrowRight) {
        paddle.direction = 1.
    }

    if keyboard_input.any_just_released([KeyCode::ArrowLeft, KeyCode::ArrowRight]) {
        paddle.direction = 0.
    }
}
