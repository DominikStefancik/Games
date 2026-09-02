use bevy::{
    app::{App, Plugin, Startup},
    ecs::schedule::IntoScheduleConfigs,
};

mod components;
mod constants;
mod helpers;
mod levels;
mod resources;
mod systems;

pub use components::*;
pub use constants::*;
pub use helpers::*;
pub use levels::*;
pub use resources::*;
pub use systems::*;

pub struct GamePlugin;

impl Plugin for GamePlugin {
    fn build(&self, app: &mut App) {
        app.insert_resource(GameInfo::init())
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
