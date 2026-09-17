use bevy::{
    app::{App, FixedUpdate, Plugin, Startup},
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
        app.add_systems(Startup, spawn_paddle).add_systems(
            FixedUpdate,
            move_paddle
                .run_if(in_state(GameState::BallReady).or_else(in_state(GameState::Running))),
        );
    }
}
