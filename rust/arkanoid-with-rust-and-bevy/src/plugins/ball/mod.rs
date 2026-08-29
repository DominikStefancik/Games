mod components;
mod constants;
mod helpers;
mod systems;

use bevy::app::{App, Plugin, Startup, Update};

pub use components::*;
pub use constants::*;
pub use helpers::*;
pub use systems::*;

pub struct BallPlugin;

impl Plugin for BallPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Startup, spawn_ball)
            .add_systems(Update, move_ball);
    }
}
