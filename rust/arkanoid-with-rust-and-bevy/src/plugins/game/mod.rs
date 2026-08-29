use bevy::app::{App, Plugin, Startup};

mod constants;
mod resources;
mod systems;

pub use constants::*;
pub use resources::*;
pub use systems::*;

pub struct GamePlugin;

impl Plugin for GamePlugin {
    fn build(&self, app: &mut App) {
        app.insert_resource(MovingArea::new())
            .add_systems(Startup, spawn_background);
    }
}
