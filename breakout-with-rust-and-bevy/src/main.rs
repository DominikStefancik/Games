mod components;
mod constants;

use crate::constants::{PADDLE_COLOR, PADDLE_SIZE, PADDLE_START_Y};
use bevy::prelude::*;
use bevy::DefaultPlugins;

/*
 * Bevy uses Entity-Component-System (ECS) architecture:
 *  Entity - represents any object in the system (game), identified by its ID
 *  Component - data related to a particular entity (position, rotation, scale, ...)
 *  System - code (functions) which operates on components
 */
fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .insert_resource(ClearColor(Color::rgb(0.9, 0.9, 0.9)))
        .add_systems(Startup, setup_system)
        .add_systems(Update, bevy::window::close_on_esc)
        .run();
}

// Bevy systems are just functions which receive special parameters
// Bevy will inject the required parameters for system functions for us
fn setup_system(mut commands: Commands) {
    // we have to spawn a camera first so we can see our player
    // if we didn't do that, the game screen will just be black
    // Note: Bundles are used for adding multiple components at once
    commands.spawn(Camera2dBundle::default());

    commands.spawn(SpriteBundle {
        transform: Transform {
            translation: Vec3::new(0., PADDLE_START_Y, 0.),
            ..Default::default()
        },
        sprite: Sprite {
            color: PADDLE_COLOR,
            custom_size: Some(PADDLE_SIZE),
            ..Default::default()
        },
        ..Default::default()
    });
}
