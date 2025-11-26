use bevy::{
    app::{App, FixedUpdate, Startup},
    state::app::AppExtStates,
};

use crate::{
    app_states::{AppState, move_to_game_over_state, move_to_game_state},
    entities::systems::run_animations,
    game::GamePlugin,
    main_menu::MainMenuPlugin,
    scenes::systems::spawn_camera,
    sonic::SonicPlugin,
};

mod app_states;
mod entities;
mod game;
mod main_menu;
mod plugins;
mod ring;
mod scenes;
mod sonic;

fn main() {
    App::new()
        .add_plugins(plugins::default::plugin)
        .init_state::<AppState>() // Alternatively we could use .insert_state(AppState::MainMenu)
        .add_plugins(MainMenuPlugin)
        .add_plugins(GamePlugin)
        .add_plugins(SonicPlugin)
        .add_systems(Startup, spawn_camera)
        .add_systems(
            FixedUpdate,
            (run_animations, move_to_game_state, move_to_game_over_state),
        )
        .run();
}
