mod components;
mod constants;
mod helpers;
mod systems;

use bevy::{
    app::{App, Plugin, Startup, Update},
    ecs::schedule::IntoScheduleConfigs,
    state::condition::in_state,
};

pub use components::*;
pub use constants::*;
pub use helpers::*;
pub use systems::*;

use crate::plugins::GameState;

pub struct BallPlugin;

impl Plugin for BallPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Startup, spawn_ball).add_systems(
            Update,
            (
                move_ball,
                check_ball_collision.run_if(in_state(GameState::Running)),
            )
                .chain(),
        );
    }
}
