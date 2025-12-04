use bevy::{
    app::{App, FixedUpdate},
    ecs::schedule::IntoScheduleConfigs,
    prelude::Plugin,
    state::{
        app::AppExtStates,
        condition::in_state,
        state::{OnEnter, OnExit, States},
    },
};

use crate::{
    app_states::AppState,
    entities::{motobug::MotobugPlugin, ring::RingPlugin},
    game::systems::{
        despawn_score_text, pause_background_music, reset_game_settings, spawn_background_music,
        spawn_score_text, toggle_pausing_game, update_game_score_text,
    },
    scene::systems::{
        despawn_backgrounds, despawn_platforms, scroll_background, scroll_platform,
        spawn_background, spawn_platform,
    },
};

pub mod components;
pub mod events;
pub mod systems;

pub struct GamePlugin;

#[derive(States, Debug, Clone, Copy, Eq, PartialEq, Hash, Default)]
pub enum GameState {
    // this says Running will be a default state of the game when we move to the Game state in our app
    #[default]
    Running,
    Paused,
}

impl Plugin for GamePlugin {
    fn build(&self, app: &mut App) {
        app.init_state::<GameState>() // Alternatively we could use .insert_state(GameState::Running)
            .add_plugins(RingPlugin)
            .add_plugins(MotobugPlugin)
            .add_systems(
                OnEnter(AppState::Game),
                (
                    spawn_background,
                    spawn_platform,
                    spawn_score_text,
                    spawn_background_music,
                    reset_game_settings,
                ),
            )
            .add_systems(
                OnExit(AppState::Game),
                (despawn_backgrounds, despawn_platforms, despawn_score_text),
            )
            .add_systems(
                FixedUpdate,
                (scroll_background, scroll_platform)
                    .run_if(in_state(AppState::Game))
                    .run_if(in_state(GameState::Running)),
            )
            .add_systems(
                FixedUpdate,
                (
                    toggle_pausing_game.run_if(in_state(AppState::Game)),
                    pause_background_music,
                ),
            )
            // Global observers
            .add_observer(update_game_score_text);
    }
}
