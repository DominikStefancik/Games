use bevy::{
    app::{App, Plugin, Startup, Update},
    ecs::schedule::IntoScheduleConfigs,
    state::state::{OnEnter, OnExit},
};

use crate::plugins::{
    shared::GameState,
    window::systems::{
        draw_background, draw_canvas, draw_instructions, hide_game_over_text, show_game_over_text,
        show_game_starting_text, update_game_starting_text,
    },
};

mod components;
mod systems;

pub use components::*;

pub struct WindowPlugin;

impl Plugin for WindowPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(
            Startup,
            (draw_background, draw_canvas, draw_instructions).chain(),
        )
        .add_systems(OnEnter(GameState::GameStarting), show_game_starting_text)
        .add_systems(OnEnter(GameState::GameOver), show_game_over_text)
        .add_systems(OnExit(GameState::GameOver), hide_game_over_text)
        .add_systems(Update, update_game_starting_text);
    }
}
