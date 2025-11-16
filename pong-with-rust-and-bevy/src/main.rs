use bevy::{
    app::{App, FixedUpdate, Startup},
    ecs::system::Commands,
};

use crate::{ball::spawn_ball_system, systems::project_positions};

mod ball;
mod components;
mod plugins;
mod spawn_helpers;
mod systems;

fn main() {
    App::new()
        .add_plugins(plugins::default::plugin)
        .add_systems(Startup, (setup_system, spawn_ball_system))
        .add_systems(FixedUpdate, project_positions)
        .run();
}

fn setup_system(mut commands: Commands) {
    spawn_helpers::spawn_camera(&mut commands);
    // we don't have to create an empty entity if we don't need it
    // here it is just for learning purposes
    spawn_helpers::spawn_empty_entity(&mut commands);
}
