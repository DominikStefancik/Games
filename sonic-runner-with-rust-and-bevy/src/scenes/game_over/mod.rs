use bevy::{
    app::App,
    ecs::schedule::IntoScheduleConfigs,
    prelude::Plugin,
    state::state::{OnEnter, OnExit},
};

use crate::{
    app_states::AppState,
    scenes::game_over::systems::{despawn_game_over_text, spawn_game_over_text, update_best_score},
};

mod components;
mod helpers;
mod systems;

pub struct GameOverPlugin;

impl Plugin for GameOverPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(
            OnEnter(AppState::GameOver),
            (
                update_best_score,
                spawn_game_over_text.after(update_best_score),
            ),
        )
        .add_systems(OnExit(AppState::GameOver), despawn_game_over_text);
    }
}
