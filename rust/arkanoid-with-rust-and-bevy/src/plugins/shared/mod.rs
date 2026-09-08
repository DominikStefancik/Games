use bevy::{
    app::{App, Plugin, PreStartup, Startup, Update},
    ecs::schedule::IntoScheduleConfigs,
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

use crate::plugins::finish_loading;

pub struct SharedPlugin;

impl Plugin for SharedPlugin {
    fn build(&self, app: &mut App) {
        app.insert_resource(Randomizer::new())
            .add_systems(PreStartup, load_textures)
            .add_systems(Startup, (finish_loading, spawn_camera).chain())
            .add_systems(Update, apply_box_texture_resize);
    }
}
