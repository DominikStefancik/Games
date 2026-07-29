use std::collections::VecDeque;

use crate::plugins::{
    game::GameState,
    shared::{DirectionQueue, SNAKE_MOVE_INTERVAL},
};
use bevy::{
    app::{App, Plugin, Update},
    ecs::schedule::IntoScheduleConfigs,
    state::condition::in_state,
    time::{Timer, TimerMode},
};

mod components;
mod helpers;
mod resources;
mod systems;

pub use components::*;
pub use helpers::*;
pub use resources::*;
pub use systems::*;

pub struct SnakePlugin;

impl Plugin for SnakePlugin {
    fn build(&self, app: &mut App) {
        app.init_resource::<Snake>()
            .insert_resource(SnakeMoveTimer(Timer::from_seconds(
                SNAKE_MOVE_INTERVAL,
                TimerMode::Repeating,
            )))
            .insert_resource(DirectionQueue(VecDeque::new()))
            .add_systems(Update, move_snake.run_if(in_state(GameState::Playing)))
            // Global observers
            .add_observer(initialise_snake);
    }
}
