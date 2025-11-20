use bevy::app::{App, FixedUpdate};

use crate::{entities::systems::run_animations, plugins::scene::ScenePlugin};

mod entities;
mod plugins;

fn main() {
    App::new()
        .add_plugins(plugins::default::plugin)
        .add_plugins(ScenePlugin)
        .add_systems(FixedUpdate, run_animations)
        .run();
}
