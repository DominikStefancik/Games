use bevy::{
    app::{App, FixedUpdate, Startup},
    state::app::AppExtStates,
};

use crate::{
    app_states::{AppState, move_to_game_over_state, move_to_game_state},
    entities::systems::run_animations,
    game::GamePlugin,
    main_menu::MainMenuPlugin,
    resources::GameSettings,
    sonic::SonicPlugin,
    systems::{load_fonts, load_sounds, load_textures, spawn_camera},
};

mod app_states;
mod entities;
mod game;
mod main_menu;
mod plugins;
mod resources;
mod ring;
mod scene;
mod sonic;
mod systems;

fn main() {
    App::new()
        .add_plugins(plugins::default::plugin)
        .insert_resource(GameSettings::new())
        .init_state::<AppState>() // Alternatively we could use .insert_state(AppState::MainMenu)
        .add_plugins(MainMenuPlugin)
        .add_plugins(GamePlugin)
        .add_plugins(SonicPlugin)
        .add_systems(
            Startup,
            (spawn_camera, load_textures, load_fonts, load_sounds),
        )
        .add_systems(
            FixedUpdate,
            (run_animations, move_to_game_state, move_to_game_over_state),
        )
        .run();
}
