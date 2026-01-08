use bevy::{
    app::{App, FixedUpdate, Startup},
    ecs::schedule::IntoScheduleConfigs,
    state::{app::AppExtStates, condition::in_state},
};

use crate::{
    app_states::{AppState, move_to_game_over_state, move_to_game_state},
    entities::{sonic::SonicPlugin, systems::run_animations},
    resources::{GameSettings, GameSpeedTimer},
    scenes::{
        game::{GamePlugin, GameState},
        game_over::GameOverPlugin,
        main_menu::MainMenuPlugin,
    },
    systems::{increase_game_speed, load_fonts, load_sounds, load_textures, spawn_camera},
};

mod app_states;
mod entities;
mod plugins;
mod resources;
mod scenes;
mod systems;

fn main() {
    App::new()
        .add_plugins(plugins::default::plugin)
        .insert_resource(GameSettings::new())
        .insert_resource(GameSpeedTimer::new())
        .init_state::<AppState>() // Alternatively we could use .insert_state(AppState::MainMenu)
        .add_plugins(MainMenuPlugin)
        .add_plugins(GamePlugin)
        .add_plugins(GameOverPlugin)
        .add_plugins(SonicPlugin)
        .add_systems(
            Startup,
            (spawn_camera, load_textures, load_fonts, load_sounds),
        )
        .add_systems(
            FixedUpdate,
            (
                run_animations,
                move_to_game_state,
                move_to_game_over_state,
                increase_game_speed
                    .run_if(in_state(AppState::Game))
                    .run_if(in_state(GameState::Running)),
            ),
        )
        .run();
}
