use bevy::app::{App, Plugin, Startup};

mod components;
mod helpers;
mod resources;
pub mod systems;

pub use components::*;
pub use helpers::*;
pub use resources::*;
pub use systems::*;

pub struct FoodPlugin;

impl Plugin for FoodPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Startup, setup_food)
            // Global observers
            .add_observer(initialise_food)
            .add_observer(create_new_food);
    }
}
