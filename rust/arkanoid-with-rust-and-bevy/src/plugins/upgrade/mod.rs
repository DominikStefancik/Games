mod components;
mod constants;
mod events;
mod helpers;
mod systems;

use bevy::{
    app::{App, Plugin, Update},
    ecs::schedule::IntoScheduleConfigs,
    state::condition::in_state,
};

pub use components::*;
pub use constants::*;
pub use events::*;
pub use helpers::*;
pub use systems::*;

use crate::plugins::GameState;

pub struct UpgradePlugin;

impl Plugin for UpgradePlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(
            Update,
            (move_upgrade, check_upgrade_collision)
                .chain()
                .run_if(in_state(GameState::Running)),
        )
        // Global observers
        .add_observer(spawn_upgrade);
    }
}
