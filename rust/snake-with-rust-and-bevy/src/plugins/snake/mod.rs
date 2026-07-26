use bevy::{
    app::{App, Plugin, Update},
    ecs::schedule::IntoScheduleConfigs,
    state::condition::in_state,
};

use crate::plugins::shared::GameState;

mod components;
mod helpers;
pub mod resources;
mod systems;

pub use helpers::*;
pub use resources::*;
pub use systems::*;

pub struct SnakePlugin;

impl Plugin for SnakePlugin {
    fn build(&self, app: &mut App) {
        app.init_resource::<Snake>()
            .add_systems(Update, move_snake.run_if(in_state(GameState::Playing)))
            // Global observers
            .add_observer(initialise_snake);
    }
}
