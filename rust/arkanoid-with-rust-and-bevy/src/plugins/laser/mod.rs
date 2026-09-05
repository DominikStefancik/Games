use bevy::{
    app::{App, Plugin, Update},
    ecs::schedule::IntoScheduleConfigs,
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

pub struct LaserPlugin;

impl Plugin for LaserPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(
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
