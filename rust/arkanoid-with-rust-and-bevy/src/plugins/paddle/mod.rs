use bevy::app::{App, Plugin, Startup, Update};

mod components;
mod constants;
mod helpers;
mod systems;

pub use components::*;
pub use constants::*;
pub use helpers::*;
pub use systems::*;

pub struct PaddlePlugin;

impl Plugin for PaddlePlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Startup, spawn_paddle)
            .add_systems(Update, move_paddle)
            // Global observers
            .add_observer(spawn_laser);
    }
}
