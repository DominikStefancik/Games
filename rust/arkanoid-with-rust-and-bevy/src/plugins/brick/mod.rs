use bevy::{
    app::{App, Plugin},
    state::state::OnEnter,
};

mod components;
mod constants;
mod events;
mod helpers;
mod systems;
mod types;

pub use components::*;
pub use constants::*;
pub use events::*;
pub use helpers::*;
pub use systems::*;
pub use types::*;

use crate::plugins::GameState;

pub struct BrickPlugin;

impl Plugin for BrickPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(OnEnter(GameState::NewLevelStarting), spawn_bricks)
            // Global observers
            .add_observer(update_or_destroy_brick);
    }
}
