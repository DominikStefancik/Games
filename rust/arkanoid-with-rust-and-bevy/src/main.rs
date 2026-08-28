use bevy::app::App;

use crate::plugins::{GamePlugin, SharedPlugin, default_plugin};

mod plugins;

fn main() {
    App::new()
        .add_plugins(default_plugin)
        .add_plugins((SharedPlugin, GamePlugin))
        .run();
}
