use bevy::app::{App, Plugin, Update};

mod systems;

pub use systems::*;

pub struct ControlsPlugin;

impl Plugin for ControlsPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(
            Update,
            (
                update_paddle_direction_on_keypress,
                update_ball_direction_on_keypress,
                start_game_on_keypress,
                toggle_pausing_game_on_keypress,
            ),
        );
    }
}
