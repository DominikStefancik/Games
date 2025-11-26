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
    game::systems::toggle_pausing_game,
    scenes::systems::{
        despawn_backgrounds, despawn_platforms, scroll_background, scroll_platform,
        spawn_background, spawn_platform,
    },
    sonic::systems::{despawn_sonic, spawn_sonic},
};

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
        app.init_state::<GameState>() // Alternatively we could use .insert_state(GameState::Running)
            .add_systems(
                OnEnter(AppState::Game),
                (spawn_background, spawn_platform, spawn_sonic),
            )
            .add_systems(
                OnExit(AppState::MainMenu),
                (despawn_backgrounds, despawn_platforms, despawn_sonic),
            )
            .add_systems(
                FixedUpdate,
                (
                    scroll_background
                        .run_if(in_state(AppState::Game))
                        .run_if(in_state(GameState::Running)),
                    scroll_platform
                        .run_if(in_state(AppState::Game))
                        .run_if(in_state(GameState::Running)),
                    toggle_pausing_game.run_if(in_state(AppState::Game)),
                ),
            );
    }
}
