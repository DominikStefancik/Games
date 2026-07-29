use bevy::{
    app::{App, Plugin, Startup, Update},
    state::state::OnEnter,
    time::{Timer, TimerMode},
};

use crate::plugins::{
    camera::{
        resources::ScreenShake,
        systems::{apply_screenshake, reset_screenshake_timer, spawn_camera},
    },
    game::GameState,
};

mod resources;
mod systems;

pub struct CameraPlugin;

impl Plugin for CameraPlugin {
    fn build(&self, app: &mut App) {
        // Initialize the screenshake timer as already finished so it doesn't
        // fire on startup. We reset it manually when the player dies.
        app.insert_resource(ScreenShake({
            let mut timer = Timer::from_seconds(0.3, TimerMode::Once);
            timer.finish();
            timer
        }))
        .add_systems(OnEnter(GameState::GameOver), reset_screenshake_timer)
        .add_systems(Startup, spawn_camera)
        .add_systems(Update, apply_screenshake);
    }
}
