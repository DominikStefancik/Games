use bevy::app::{App, Plugin, Startup};

use crate::plugins::snake::systems::{initialise_snake, setup_snake};

pub mod resources;
mod systems;

pub struct SnakePlugin;

impl Plugin for SnakePlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Startup, setup_snake)
            // Global observers
            .add_observer(initialise_snake);
    }
}
