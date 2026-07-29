use bevy::app::{App, Plugin, Startup};

mod components;
mod constants;
mod helpers;
mod resources;
mod systems;

/* when exporting public items from each submodule here, we hide the implementation details where the items come from
 * e.g. when importing a constant from "constants" submodule, the import statemment will be
 *
 * "use crate::plugins::shared::GRID_SIZE;" instead of "use crate::plugins::shared::constants::GRID_SIZE;"
 *
 * That way the outside world doesn't know that the GRID_SIZE constant comes from the "constants" submodule
 */
pub use components::*;
pub use constants::*;
pub use helpers::*;
pub use resources::*;
pub use systems::*;

pub struct SharedPlugin;

impl Plugin for SharedPlugin {
    fn build(&self, app: &mut App) {
        // the GameFonts is initialised by calling the "from_world" method
        app.init_resource::<GameFonts>() // calls GameFonts::from_world internally
            .insert_resource(Grid::default())
            .insert_resource(Randomizer {
                rng: rand::make_rng(),
            })
            .add_systems(Startup, load_sounds);
    }
}
