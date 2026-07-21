use bevy::app::{App, Plugin, Startup};

use crate::plugins::food::systems::{initialise_food, setup_food};

mod helpers;
mod resources;
pub mod systems;

pub struct FoodPlugin;

impl Plugin for FoodPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Startup, setup_food)
            // Global observers
            .add_observer(initialise_food);
    }
}
