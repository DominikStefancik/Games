use bevy::{
    app::{App, Plugin, Startup},
    ecs::schedule::IntoScheduleConfigs,
    state::app::AppExtStates,
};

mod components;
mod constants;
mod helpers;
mod levels;
mod resources;
mod states;
mod systems;

pub use components::*;
pub use constants::*;
pub use helpers::*;
pub use levels::*;
pub use resources::*;
pub use states::*;
pub use systems::*;

pub struct GamePlugin;

impl Plugin for GamePlugin {
    fn build(&self, app: &mut App) {
        app.init_state::<GameState>()
            .insert_resource(GameInfo::init())
            .insert_resource(MovingArea::new())
            .add_systems(
                Startup,
                (spawn_background, spawn_score_text, spawn_hearts).chain(),
            )
            // Global observers
            .add_observer(spawn_new_heart)
            .add_observer(update_score);
    }
}
