use bevy::{
    app::{App, Plugin, Startup, Update},
    ecs::schedule::{IntoScheduleConfigs, SystemCondition},
    state::condition::in_state,
};

mod components;
mod constants;
mod events;
mod helpers;
mod systems;

pub use components::*;
pub use constants::*;
pub use events::*;
pub use helpers::*;
pub use systems::*;

use crate::plugins::GameState;

pub struct PaddlePlugin;

impl Plugin for PaddlePlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Startup, spawn_paddle)
            .add_systems(
                Update,
                move_paddle.run_if(
                    in_state(GameState::GameStarting).or_else(in_state(GameState::Running)),
                ),
            )
            .add_systems(
                Update,
                (
                    adjust_lasers_position,
                    move_projectile,
                    check_projectile_collision.after(move_projectile),
                )
                    .run_if(in_state(GameState::Running)),
            )
            // Global observers
            .add_observer(spawn_laser)
            .add_observer(spawn_projectiles);
    }
}
