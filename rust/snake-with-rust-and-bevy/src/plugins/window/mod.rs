use bevy::{
    app::{App, Plugin, Startup},
    ecs::schedule::IntoScheduleConfigs,
};

use crate::plugins::window::systems::{draw_background, draw_canvas, draw_instructions};

mod systems;

pub struct WindowPlugin;

impl Plugin for WindowPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(
            Startup,
            (draw_background, draw_canvas, draw_instructions).chain(),
        );
    }
}
