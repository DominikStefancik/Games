mod components;
mod constants;
mod events;
mod helpers;
mod systems;

use bevy::app::{App, Plugin, Startup};

pub use components::*;
pub use constants::*;
pub use events::*;
pub use helpers::*;
pub use systems::*;

pub struct BrickPlugin;

impl Plugin for BrickPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Startup, spawn_bricks);
    }
}
