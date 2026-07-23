use bevy::{
    app::{App, Plugin, Startup},
    ecs::schedule::IntoScheduleConfigs,
};

mod components;
mod helpers;
mod resources;
mod systems;

pub use components::*;
pub use helpers::*;
pub use resources::*;
pub use systems::*;

use crate::core::load_fonts;

pub struct ScorePlugin;

impl Plugin for ScorePlugin {
    fn build(&self, app: &mut App) {
        app.insert_resource(Score::default())
            .add_systems(Startup, spawn_score.after(load_fonts))
            .add_observer(update_score);
    }
}
