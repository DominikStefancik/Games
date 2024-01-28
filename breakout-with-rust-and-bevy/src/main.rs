mod components;
mod constants;
mod helpers;
mod systems;

use crate::constants::BACKGROUND_COLOR;
use crate::helpers::{spawn_ball, spawn_player, spawn_wall};
use crate::systems::{ball_velocity_system, move_paddle_system};
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
        .insert_resource(ClearColor(BACKGROUND_COLOR))
        .add_systems(Startup, setup_system)
        .add_systems(Update, bevy::window::close_on_esc)
        // FixedUpdate always runs on a fixed rate; by default it is 60 frames per second
        .add_systems(FixedUpdate, (move_paddle_system, ball_velocity_system))
        .run();
}

// Bevy systems are just functions which receive special parameters
// Bevy will inject the required parameters for system functions for us
fn setup_system(
    mut commands: Commands,
    meshes: ResMut<Assets<Mesh>>,
    materials: ResMut<Assets<ColorMaterial>>,
) {
    // we have to spawn a camera first so we can see our player
    // if we didn't do that, the game screen will just be black
    // Note: Bundles are used for adding multiple components at once
    commands.spawn(Camera2dBundle::default());

    spawn_wall(&mut commands);
    spawn_player(&mut commands);
    spawn_ball(&mut commands, meshes, materials);
}
