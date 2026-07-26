use std::collections::VecDeque;

use bevy::{
    app::{App, Plugin, Startup, Update},
    ecs::schedule::IntoScheduleConfigs,
    state::{app::AppExtStates, condition::in_state},
    time::{Timer, TimerMode},
};

use crate::core::{
    DirectionQueue, GAME_STARTING_INTERVAL, GameFonts, Grid, MoveTimer, Randomizer,
    SNAKE_MOVE_INTERVAL, load_sounds,
};

pub mod events;
mod helpers;
mod resources;
mod states;
pub mod systems;

pub use events::*;
pub use helpers::*;
pub use resources::*;
pub use states::*;
pub use systems::*;

pub struct SharedPlugin;

impl Plugin for SharedPlugin {
    fn build(&self, app: &mut App) {
        app.init_state::<GameState>()
            // the GameFonts is initialised by calling the "from_world" method
            .init_resource::<GameFonts>()
            .insert_resource(Grid::default())
            .insert_resource(Randomizer {
                rng: rand::make_rng(),
            })
            .insert_resource(GameStartingTimer(Timer::from_seconds(
                GAME_STARTING_INTERVAL,
                TimerMode::Once,
            )))
            .insert_resource(MoveTimer(Timer::from_seconds(
                SNAKE_MOVE_INTERVAL,
                TimerMode::Repeating,
            )))
            .insert_resource(DirectionQueue(VecDeque::new()))
            .add_systems(Startup, load_sounds)
            .add_systems(
                Update,
                (
                    move_to_playing_state,
                    toggle_pausing_game.run_if(in_state(GameState::Playing)),
                ),
            );
    }
}
