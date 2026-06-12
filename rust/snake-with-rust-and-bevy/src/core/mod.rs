pub mod components;
pub mod constants;
pub mod resources;
pub mod systems;

/* when exporting public items from each submodule here, we hide the implementation details where the items come from
 * e.g. when importing a constant from "constants" submodule, the import statemment will be
 *
 * "use crate::core::GRID_SIZE;" instead of "use crate::core::constants::GRID_SIZE;"
 *
 * That way the outside world doesn't know that the GRID_SIZE constant comes from the "constants" submodule
 */
pub use components::*;
pub use constants::*;
pub use resources::*;
pub use systems::*;
