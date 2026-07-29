use bevy::app::App;

use crate::plugins::{
    CameraPlugin, ControlsPlugin, FoodPlugin, GamePlugin, ScorePlugin, SharedPlugin, SnakePlugin,
    WindowPlugin, default_plugin,
};

mod plugins;

fn main() {
    App::new()
        .add_plugins(default_plugin)
        .add_plugins((
            CameraPlugin,
            SharedPlugin,
            WindowPlugin,
            ScorePlugin,
            ControlsPlugin,
            GamePlugin,
            SnakePlugin,
            FoodPlugin,
        ))
        .run();
}
