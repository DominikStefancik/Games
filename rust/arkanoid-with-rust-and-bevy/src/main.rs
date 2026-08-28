use bevy::app::App;

use crate::plugins::default_plugin;

mod plugins;

fn main() {
    App::new().add_plugins(default_plugin).run();
}
