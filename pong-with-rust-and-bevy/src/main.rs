use bevy::{
    app::{App, FixedUpdate, Startup},
    ecs::{schedule::IntoScheduleConfigs, system::Commands},
};

use crate::{
    ball::systems::{move_ball_system, spawn_ball_system},
    collision::handle_collisions_system,
    paddle::systems::spawn_paddles_system,
    systems::project_positions,
};

mod ball;
mod collision;
mod components;
mod paddle;
mod plugins;
mod spawn_helpers;
mod systems;

fn main() {
    App::new()
        .add_plugins(plugins::default::plugin)
        .add_systems(
            Startup,
            (setup_system, spawn_ball_system, spawn_paddles_system),
        )
        .add_systems(
            FixedUpdate,
            (
                project_positions,
                // We add "move_ball" system to run before
                // we project our positions so we are not reading movement one frame behind
                move_ball_system.before(project_positions),
                handle_collisions_system.after(move_ball_system),
            ),
        )
        .run();
}

fn setup_system(mut commands: Commands) {
    spawn_helpers::spawn_camera(&mut commands);
    // we don't have to create an empty entity if we don't need it
    // here it is just for learning purposes
    spawn_helpers::spawn_empty_entity(&mut commands);
}
