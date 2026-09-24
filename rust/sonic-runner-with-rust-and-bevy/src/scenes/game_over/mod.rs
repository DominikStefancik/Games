use bevy::{
    app::{App, FixedUpdate},
    ecs::schedule::IntoScheduleConfigs,
    prelude::Plugin,
    state::state::{OnEnter, OnExit},
    time::{Timer, TimerMode},
};

use crate::{
    app_states::AppState,
    scenes::game_over::{
        resources::PlayAgainCooldownTimer,
        systems::{
            despawn_game_over_text, reset_play_again_instructions_timer, spawn_game_over_text,
            spawn_play_again_instructions_text, update_best_score, update_curent_rank,
        },
    },
};

mod components;
mod helpers;
pub mod resources;
mod systems;

pub struct GameOverPlugin;

impl Plugin for GameOverPlugin {
    fn build(&self, app: &mut App) {
        app.insert_resource(PlayAgainCooldownTimer(Timer::from_seconds(
            1.5,
            TimerMode::Once,
        )))
        .add_systems(
            OnEnter(AppState::GameOver),
            (
                (update_best_score, update_curent_rank).before(spawn_game_over_text),
                spawn_game_over_text,
                reset_play_again_instructions_timer,
            ),
        )
        .add_systems(OnExit(AppState::GameOver), despawn_game_over_text)
        .add_systems(FixedUpdate, spawn_play_again_instructions_text);
    }
}
