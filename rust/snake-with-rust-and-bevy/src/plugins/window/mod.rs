use bevy::{
    app::{App, Plugin, Startup, Update},
    ecs::schedule::IntoScheduleConfigs,
};

use crate::plugins::window::systems::{
    draw_background, draw_canvas, draw_instructions, spawn_game_starting_text,
    update_game_starting_text,
};

mod components;
mod systems;

pub struct WindowPlugin;

impl Plugin for WindowPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(
            Startup,
            (
                draw_background,
                draw_canvas,
                draw_instructions,
                spawn_game_starting_text,
            )
                .chain(),
        )
        .add_systems(Update, update_game_starting_text);
    }
}
