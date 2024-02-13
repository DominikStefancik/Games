mod components;
mod constants;
mod helpers;
mod resources;
mod systems;

use crate::constants::BACKGROUND_COLOR;
use crate::helpers::{spawn_ball, spawn_bricks, spawn_player, spawn_scoreboard, spawn_wall};
use crate::resources::{CollisionSound, Scoreboard};
use crate::systems::{
    ball_velocity_system, check_ball_collisions_system, move_paddle_system,
    update_scoreboard_system,
};
use bevy::prelude::*;
use bevy::DefaultPlugins;

/*
 * Bevy uses Entity-Component-System (ECS) architecture:
 *  Entity - represents any object in the system (game),
 *           identified by its ID and is tied to a group of components
 *  Component - data related to a particular entity (position, rotation, scale, ...)
 *  System - code (functions) which operates on components
 */
fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .insert_resource(ClearColor(BACKGROUND_COLOR))
        // we have to add a resource into the Bevy "world" if later we want to access it in a system function
        .insert_resource(Scoreboard { score: 0 })
        .add_systems(Startup, setup_system)
        .add_systems(Update, bevy::window::close_on_esc)
        // FixedUpdate always runs on a fixed rate; by default it is 60 frames per second
        .add_systems(
            FixedUpdate,
            (
                move_paddle_system,
                ball_velocity_system,
                // we want the "check_ball_collisions_system" to run after the "ball_velocity_system" runs
                check_ball_collisions_system.after(ball_velocity_system),
                update_scoreboard_system,
            ),
        )
        .run();
}

// Bevy systems are just functions which receive special parameters
// Bevy will inject the required parameters for system functions for us
fn setup_system(
    mut commands: Commands,
    meshes: ResMut<Assets<Mesh>>,
    materials: ResMut<Assets<ColorMaterial>>,
    asset_server: Res<AssetServer>,
) {
    // we have to spawn a camera first, so we can see our player
    // if we didn't do that, the game screen will just be black
    // Note: Bundles are used for adding multiple components at once
    commands.spawn(Camera2dBundle::default());

    // we have to insert a sound as a resource in order to be able to reference it
    // in the "check_ball_collisions_system"
    let ball_collision_sound = asset_server.load("sounds/breakout_collision.ogg");
    commands.insert_resource(CollisionSound(ball_collision_sound));

    spawn_wall(&mut commands);
    spawn_bricks(&mut commands);
    spawn_player(&mut commands);
    spawn_ball(&mut commands, meshes, materials);
    spawn_scoreboard(&mut commands);
}
