use bevy::app::App;

use crate::plugins::{CameraPlugin, SharedPlugin, WindowPlugin, default_plugin};

mod core;
mod plugins;

fn main() {
    App::new()
        .add_plugins(default_plugin)
        .add_plugins((CameraPlugin, SharedPlugin, WindowPlugin))
        .run();
}
