use bevy::app::App;

use crate::plugins::{
    BallPlugin, BrickPlugin, ControlsPlugin, GamePlugin, LaserPlugin, PaddlePlugin, SharedPlugin,
    UpgradePlugin, default_plugin,
};

mod plugins;

fn main() {
    App::new()
        .add_plugins(default_plugin)
        .add_plugins((
            SharedPlugin,
            ControlsPlugin,
            GamePlugin,
            PaddlePlugin,
            LaserPlugin,
            BallPlugin,
            BrickPlugin,
            UpgradePlugin,
        ))
        .run();
}
