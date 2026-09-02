use bevy::{
    ecs::system::{Res, ResMut, Single},
    input::{ButtonInput, keyboard::KeyCode},
    state::state::{NextState, State},
};
use rand::seq::IndexedRandom;

use crate::plugins::{BALL_MOVEMENT_SPEED, Ball, GameState, Paddle, Randomizer};

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
    app_state: Res<State<GameState>>,
    mut ball: Single<&mut Ball>,
) {
    if *app_state.get() != GameState::GameStarting {
        return;
    }

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

pub fn start_game_on_keypress(
    keyboard_input: Res<ButtonInput<KeyCode>>,
    app_state: Res<State<GameState>>,
    mut next_state: ResMut<NextState<GameState>>,
    mut randomizer: ResMut<Randomizer>,
    mut ball: Single<&mut Ball>,
) {
    if *app_state.get() != GameState::GameStarting {
        return;
    }

    let choices: [f32; 2] = [-1., 1.];

    if keyboard_input.just_pressed(KeyCode::Space) {
        ball.direction.x = *choices.choose(&mut randomizer.rng).unwrap();
        ball.direction.y = 1.;
        ball.speed = BALL_MOVEMENT_SPEED;
        next_state.set(GameState::Running);
    }
}

pub fn toggle_pausing_game_on_keypress(
    keyboard_input: Res<ButtonInput<KeyCode>>,
    app_state: Res<State<GameState>>,
    mut next_state: ResMut<NextState<GameState>>,
) {
    if keyboard_input.just_pressed(KeyCode::KeyP) {
        if *app_state.get() == GameState::Running {
            next_state.set(GameState::Paused);
        } else if *app_state.get() == GameState::Paused {
            next_state.set(GameState::Running);
        }
    }
}
