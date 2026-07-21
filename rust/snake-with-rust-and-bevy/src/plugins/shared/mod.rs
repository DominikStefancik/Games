use bevy::app::{App, Plugin, Startup};

use crate::core::{Grid, Randomizer, load_fonts};

pub mod events;
pub mod systems;

pub use events::*;
pub use systems::*;

pub struct SharedPlugin;

impl Plugin for SharedPlugin {
    fn build(&self, app: &mut App) {
        app.insert_resource(Grid::default())
            .insert_resource(Randomizer {
                rng: rand::make_rng(),
            })
            .add_systems(Startup, load_fonts);
    }
}
