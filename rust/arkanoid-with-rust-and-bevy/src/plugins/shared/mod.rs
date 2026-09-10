use bevy::{
    app::{App, Plugin, PreStartup, Startup, Update},
    ecs::schedule::IntoScheduleConfigs,
    state::state::OnEnter,
};

mod components;
mod constants;
mod helpers;
mod resources;
mod systems;

pub use components::*;
pub use constants::*;
pub use helpers::*;
pub use resources::*;
pub use systems::*;

use crate::plugins::{GameState, finish_loading};

pub struct SharedPlugin;

impl Plugin for SharedPlugin {
    fn build(&self, app: &mut App) {
        app.insert_resource(Randomizer::new())
            .add_systems(PreStartup, (load_textures, load_sounds))
            .add_systems(
                Startup,
                (finish_loading, spawn_camera, spawn_background_music).chain(),
            )
            .add_systems(Update, apply_box_texture_resize)
            .add_systems(OnEnter(GameState::Running), play_backround_music)
            .add_systems(OnEnter(GameState::GameWin), stop_backround_music)
            .add_systems(OnEnter(GameState::GameOver), stop_backround_music);
    }
}
