mod components;
mod constants;
mod systems;

use bevy::app::{App, Plugin, Startup, Update};

pub use components::*;
pub use constants::*;
pub use systems::*;

pub struct PaddlePlugin;

impl Plugin for PaddlePlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Startup, spawn_paddle)
            .add_systems(Update, move_paddle);
    }
}
