use bevy::app::{App, Plugin, Startup, Update};

mod components;
mod helpers;
pub mod resources;
mod systems;

pub use helpers::*;
pub use resources::*;
pub use systems::*;

pub struct SnakePlugin;

impl Plugin for SnakePlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Startup, setup_snake)
            .add_systems(Update, move_snake)
            // Global observers
            .add_observer(initialise_snake);
    }
}
