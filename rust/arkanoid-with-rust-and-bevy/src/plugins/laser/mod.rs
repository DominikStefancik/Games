use bevy::{
    app::{App, Plugin, Update},
    ecs::schedule::IntoScheduleConfigs,
    state::condition::in_state,
    time::{Timer, TimerMode},
};

mod components;
mod constants;
mod events;
mod helpers;
mod resources;
mod systems;

pub use components::*;
pub use constants::*;
pub use events::*;
pub use helpers::*;
pub use resources::*;
pub use systems::*;

use crate::plugins::GameState;

pub struct LaserPlugin;

impl Plugin for LaserPlugin {
    fn build(&self, app: &mut App) {
        app.insert_resource(LaserCooldownTimer(Timer::from_seconds(
            0.75,
            TimerMode::Once,
        )))
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
