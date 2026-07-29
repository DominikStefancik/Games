use bevy::app::{App, Plugin, Update};

mod components;
mod events;
mod helpers;
mod resources;
mod systems;

pub use components::*;
pub use events::*;
pub use helpers::*;
pub use resources::*;
pub use systems::*;

pub struct FoodPlugin;

impl Plugin for FoodPlugin {
    fn build(&self, app: &mut App) {
        app.init_resource::<Food>()
            .add_systems(Update, update_particles)
            // Global observers
            .add_observer(initialise_food)
            .add_observer(create_new_food)
            .add_observer(spawn_food_particles);
    }
}
