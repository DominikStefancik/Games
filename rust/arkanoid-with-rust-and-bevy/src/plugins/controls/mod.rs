use bevy::{
    app::{App, Plugin, Update},
    ecs::schedule::{IntoScheduleConfigs, SystemCondition},
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
                update_ball_direction_on_keypress.run_if(in_state(GameState::BallReady)),
                shoot_projectile_on_keypress.run_if(in_state(GameState::Running)),
                start_game_on_keypress.run_if(in_state(GameState::BallReady)),
                toggle_pausing_game_on_keypress,
                restart_game_on_keypress
                    .run_if(in_state(GameState::GameWin).or_else(in_state(GameState::GameOver))),
            ),
        );
    }
}
