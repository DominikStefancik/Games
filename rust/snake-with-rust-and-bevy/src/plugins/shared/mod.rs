use std::collections::VecDeque;

use bevy::{
    app::{App, Plugin, Startup, Update},
    state::app::AppExtStates,
    time::{Timer, TimerMode},
};

use crate::core::{
    DirectionQueue, Grid, MoveTimer, Randomizer, SNAKE_MOVE_INTERVAL, load_fonts, load_sounds,
};

pub mod events;
mod helpers;
mod states;
pub mod systems;

pub use events::*;
pub use helpers::*;
pub use states::*;
pub use systems::*;

pub struct SharedPlugin;

impl Plugin for SharedPlugin {
    fn build(&self, app: &mut App) {
        app.init_state::<GameState>()
            .insert_resource(Grid::default())
            .insert_resource(Randomizer {
                rng: rand::make_rng(),
            })
            .insert_resource(MoveTimer(Timer::from_seconds(
                SNAKE_MOVE_INTERVAL,
                TimerMode::Repeating,
            )))
            .insert_resource(DirectionQueue(VecDeque::new()))
            .add_systems(Startup, (load_fonts, load_sounds))
            .add_systems(Update, toggle_pausing_game);
    }
}
