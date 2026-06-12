use bevy::app::{App, Startup};

use crate::core::spawn_camera;

mod core;
mod plugins;

fn main() {
    App::new()
        .add_plugins(plugins::default::plugin)
        .add_systems(Startup, spawn_camera)
        .run();
}
