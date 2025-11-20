use bevy::app::App;

use crate::plugins::scene::ScenePlugin;

mod plugins;

fn main() {
    App::new()
        .add_plugins(plugins::default::plugin)
        .add_plugins(ScenePlugin)
        .run();
}
