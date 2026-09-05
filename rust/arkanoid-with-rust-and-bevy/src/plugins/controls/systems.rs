use bevy::{
    ecs::system::{Commands, Res, ResMut, Single},
    input::{ButtonInput, keyboard::KeyCode},
    state::state::{NextState, State},
    time::Time,
};
use rand::seq::IndexedRandom;

use crate::plugins::{
    BALL_MOVEMENT_SPEED, Ball, GameState, LaserCooldownTimer, Paddle, ProjectileShot, Randomizer,
};

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

pub fn shoot_projectile_on_keypress(
    mut commands: Commands,
    time: Res<Time>,
    mut timer: ResMut<LaserCooldownTimer>,
    keyboard_input: Res<ButtonInput<KeyCode>>,
) {
    timer.0.tick(time.delta());

    if keyboard_input.just_pressed(KeyCode::Space) && timer.0.is_finished() {
        commands.trigger(ProjectileShot);
        timer.0.reset();
    }
}

pub fn start_game_on_keypress(
    keyboard_input: Res<ButtonInput<KeyCode>>,
    mut next_state: ResMut<NextState<GameState>>,
    mut randomizer: ResMut<Randomizer>,
    mut ball: Single<&mut Ball>,
) {
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
