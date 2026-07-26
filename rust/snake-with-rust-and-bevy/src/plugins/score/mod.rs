use bevy::app::{App, Plugin, Startup, Update};

mod components;
mod helpers;
mod resources;
mod systems;

pub use components::*;
pub use helpers::*;
pub use resources::*;
pub use systems::*;

pub struct ScorePlugin;

impl Plugin for ScorePlugin {
    fn build(&self, app: &mut App) {
        app.insert_resource(Score::default())
            .add_systems(Startup, spawn_score)
            .add_systems(Update, update_score_pop)
            .add_observer(update_score)
            .add_observer(spawn_score_pop);
    }
}
