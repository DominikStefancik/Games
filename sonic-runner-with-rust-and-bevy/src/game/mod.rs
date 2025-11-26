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
    game::{resources::GameSettings, systems::toggle_pausing_game},
    ring::RingPlugin,
    scenes::systems::{
        despawn_backgrounds, despawn_platforms, scroll_background, scroll_platform,
        spawn_background, spawn_platform,
    },
};

pub mod resources;
mod systems;

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
        app.insert_resource(GameSettings::new())
            .init_state::<GameState>() // Alternatively we could use .insert_state(GameState::Running)
            .add_plugins(RingPlugin)
            .add_systems(OnEnter(AppState::Game), (spawn_background, spawn_platform))
            .add_systems(
                OnExit(AppState::Game),
                (despawn_backgrounds, despawn_platforms),
            )
            .add_systems(
                FixedUpdate,
                (scroll_background, scroll_platform)
                    .run_if(in_state(AppState::Game))
                    .run_if(in_state(GameState::Running)),
            )
            .add_systems(
                FixedUpdate,
                toggle_pausing_game.run_if(in_state(AppState::Game)),
            );
    }
}
