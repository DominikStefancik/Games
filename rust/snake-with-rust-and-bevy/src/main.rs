use bevy::app::App;

use crate::plugins::{
    CameraPlugin, ControlsPlugin, FoodPlugin, GamePlugin, SharedPlugin, SnakePlugin, WindowPlugin,
    default_plugin,
};

mod core;
mod plugins;

fn main() {
    App::new()
        .add_plugins(default_plugin)
        .add_plugins((
            CameraPlugin,
            SharedPlugin,
            WindowPlugin,
            ControlsPlugin,
            GamePlugin,
            SnakePlugin,
            FoodPlugin,
        ))
        .run();
}
