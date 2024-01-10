// use bevy::prelude::*;

use bevy::prelude::{
    App, AssetServer, Camera2dBundle, ClearColor, Color, Commands, IVec2, PluginGroup, Query, Res,
    Startup, Update, Window, WindowPlugin, WindowPosition,
};
use bevy::DefaultPlugins;
use space_invaders_with_rust_and_bevy::enemy::EnemyPlugin;
use space_invaders_with_rust_and_bevy::systems::laser_from_player_hit_enemy_system;
use space_invaders_with_rust_and_bevy::{
    assets::{ENEMY_LASER_SPRITE, ENEMY_SPRITE, PLAYER_LASER_SPRITE, PLAYER_SPRITE},
    player::PlayerPlugin,
    resources::{GameTextures, WindowSize},
    systems::movable_system,
};

// Bevy has 4 main constructs:  Entity, Component, System, Resource
fn main() {
    App::new()
        .insert_resource(ClearColor(Color::rgb(0.04, 0.04, 0.04)))
        .add_plugins(DefaultPlugins.set(WindowPlugin {
            primary_window: Some(Window {
                title: "Rust Space Invaders".to_string(),
                // property resolution is of the type WindowResolution
                // and the method "into()" automatically converts a tuple into this required type
                resolution: (598_f32, 676_f32).into(),
                ..Default::default()
            }),
            ..Default::default()
        }))
        .add_plugins(PlayerPlugin)
        .add_plugins(EnemyPlugin)
        .add_systems(Startup, setup_system)
        .add_systems(Update, movable_system)
        .add_systems(Update, laser_from_player_hit_enemy_system)
        .run();
}

// Bevy Systems

// Commands allow to put or remove things into/from the game scene
// Res as a generic type represents a resource. Bevy will look at the types, find a right resource and inject is as an argument
fn setup_system(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
    // we are gonna update the position of the game window, that's why the argument has to be mutable
    mut windows: Query<&mut Window>,
) {
    // Add camera into the scene
    // spawn_batch() allows to spawn an entity with a set of properties
    commands.spawn(Camera2dBundle::default());

    // position the game window
    let mut window = windows.single_mut();
    window.position = WindowPosition::new(IVec2::new(1980, 0));

    let window_size = WindowSize {
        width: window.resolution.width(),
        height: window.resolution.height(),
    };
    commands.insert_resource(window_size);

    let game_textures = GameTextures {
        player: asset_server.load(PLAYER_SPRITE),
        player_laser: asset_server.load(PLAYER_LASER_SPRITE),
        enemy: asset_server.load(ENEMY_SPRITE),
        enemy_laser: asset_server.load(ENEMY_LASER_SPRITE),
    };
    commands.insert_resource(game_textures);
}
