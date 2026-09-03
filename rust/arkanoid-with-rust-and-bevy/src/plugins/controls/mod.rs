use bevy::{
    app::{App, Plugin, Update},
    ecs::schedule::IntoScheduleConfigs,
    state::condition::in_state,
};

mod systems;

pub use systems::*;

use crate::plugins::GameState;

pub struct ControlsPlugin;

impl Plugin for ControlsPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(
            Update,
            (
                update_paddle_direction_on_keypress,
                update_ball_direction_on_keypress.run_if(in_state(GameState::GameStarting)),
                start_game_on_keypress.run_if(in_state(GameState::GameStarting)),
                toggle_pausing_game_on_keypress,
            ),
        );
    }
}
