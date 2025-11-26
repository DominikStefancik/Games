use bevy::app::{App, FixedUpdate};

use crate::{entities::systems::run_animations, main_menu::MainMenuPlugin};

mod entities;
mod main_menu;
mod plugins;
mod scenes;
mod sonic;

fn main() {
    App::new()
        .add_plugins(plugins::default::plugin)
        .add_plugins(MainMenuPlugin)
        .add_systems(FixedUpdate, run_animations)
        .run();
}
