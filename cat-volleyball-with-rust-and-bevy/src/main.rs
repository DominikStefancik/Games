mod constants;

use crate::constants::{ARENA_HEIGHT, ARENA_WIDTH};
use bevy::prelude::*;

fn main() {
    App::new()
        .add_plugins(DefaultPlugins.set(WindowPlugin {
            primary_window: Some(Window {
                title: "Rust Cat Volleyball".into(),
                resolution: (ARENA_WIDTH, ARENA_HEIGHT).into(),
                ..Default::default()
            }),
            ..Default::default()
        }))
        .insert_resource(ClearColor(Color::rgb(0., 0., 0.)))
        .add_systems(Startup, setup_system)
        .run()
}

fn setup_system(mut commands: Commands) {
    commands.spawn(Camera2dBundle {
        // The camera itself is centered at the middle of the arena at unit height (z-parameter) above the canvas
        transform: Transform::from_xyz(ARENA_WIDTH / 2., ARENA_HEIGHT / 2., 1.),
        ..Default::default()
    });
}
