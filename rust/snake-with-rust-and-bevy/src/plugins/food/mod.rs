use bevy::app::{App, Plugin, Startup};

mod helpers;
mod resources;
pub mod systems;

pub use systems::*;

pub struct FoodPlugin;

impl Plugin for FoodPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Startup, setup_food)
            // Global observers
            .add_observer(initialise_food);
    }
}
