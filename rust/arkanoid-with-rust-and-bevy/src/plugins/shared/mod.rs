use bevy::app::{App, Plugin, PreStartup, Startup};

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

pub struct SharedPlugin;

impl Plugin for SharedPlugin {
    fn build(&self, app: &mut App) {
        app.insert_resource(Randomizer::new())
            .add_systems(PreStartup, load_textures)
            .add_systems(Startup, spawn_camera);
    }
}
