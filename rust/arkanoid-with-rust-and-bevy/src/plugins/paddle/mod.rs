use bevy::{
    app::{App, Plugin, Startup, Update},
    ecs::schedule::{IntoScheduleConfigs, SystemCondition},
    state::condition::in_state,
};

mod components;
mod constants;
mod helpers;
mod systems;

pub use components::*;
pub use constants::*;
pub use helpers::*;
pub use systems::*;

use crate::plugins::GameState;

pub struct PaddlePlugin;

impl Plugin for PaddlePlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Startup, spawn_paddle)
            .add_systems(
                Update,
                (
                    move_paddle.run_if(
                        in_state(GameState::GameStarting).or_else(in_state(GameState::Running)),
                    ),
                    adjust_lasers_position,
                ),
            )
            // Global observers
            .add_observer(spawn_laser);
    }
}
