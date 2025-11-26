use bevy::{
    app::{App, FixedUpdate, Startup},
    state::{app::AppExtStates, state::States},
};

use crate::{
    entities::systems::run_animations, game::GamePlugin, main_menu::MainMenuPlugin,
    scenes::systems::spawn_camera,
};

mod entities;
mod game;
mod main_menu;
mod plugins;
mod scenes;
mod sonic;

#[derive(States, Debug, Clone, Copy, Eq, PartialEq, Hash, Default)]
pub enum AppState {
    // this says MainMenu will be a default state of the app when we start it
    #[default]
    MainMenu,
    Game,
    GameOver,
}

fn main() {
    App::new()
        .add_plugins(plugins::default::plugin)
        .init_state::<AppState>() // Alternatively we could use .insert_state(AppState::MainMenu)
        .add_plugins(MainMenuPlugin)
        .add_plugins(GamePlugin)
        .add_systems(Startup, spawn_camera)
        .add_systems(FixedUpdate, run_animations)
        .run();
}
