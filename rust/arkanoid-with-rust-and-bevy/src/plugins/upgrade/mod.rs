mod components;
mod constants;
mod systems;

use bevy::app::{App, Plugin, Update};

pub use components::*;
pub use constants::*;
pub use systems::*;

pub struct UpgradePlugin;

impl Plugin for UpgradePlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Update, move_upgrade)
            // Global observers
            .add_observer(spawn_upgrade);
    }
}
