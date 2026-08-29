use bevy::{
    ecs::system::{Res, ResMut, Single},
    input::{ButtonInput, keyboard::KeyCode},
};
use rand::seq::IndexedRandom;

use crate::plugins::{BALL_MOVEMENT_SPEED, Ball, Paddle, Randomizer};

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

pub fn update_ball_direction_on_keypress(
    keyboard_input: Res<ButtonInput<KeyCode>>,
    mut ball: Single<&mut Ball>,
) {
    if ball.is_stuck_to_paddle {
        if keyboard_input.just_pressed(KeyCode::ArrowLeft) {
            ball.direction.x = -1.;
        }

        if keyboard_input.just_pressed(KeyCode::ArrowRight) {
            ball.direction.x = 1.
        }

        if keyboard_input.any_just_released([KeyCode::ArrowLeft, KeyCode::ArrowRight]) {
            ball.direction.x = 0.
        }
    }
}

pub fn activate_ball_movement_on_keypress(
    keyboard_input: Res<ButtonInput<KeyCode>>,
    mut randomizer: ResMut<Randomizer>,
    mut ball: Single<&mut Ball>,
) {
    let choices: [f32; 2] = [-1., 1.];

    if ball.is_stuck_to_paddle && keyboard_input.just_pressed(KeyCode::Space) {
        ball.is_stuck_to_paddle = false;
        ball.direction.x = *choices.choose(&mut randomizer.rng).unwrap();
        ball.speed = BALL_MOVEMENT_SPEED;
    }
}
