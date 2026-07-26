use bevy::{
    app::{App, Plugin, Update},
    ecs::schedule::IntoScheduleConfigs,
    state::condition::in_state,
};

mod systems;

pub use systems::*;

use crate::plugins::shared::GameState;

pub struct ControlsPlugin;

impl Plugin for ControlsPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(
            Update,
            enqueue_snake_direction_on_keypress.run_if(in_state(GameState::Playing)),
        );
    }
}
