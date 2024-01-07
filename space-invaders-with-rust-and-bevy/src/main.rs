// use bevy::prelude::*;

use bevy::DefaultPlugins;
use bevy::prelude::{App, ClearColor, Color, PluginGroup, Window, WindowPlugin};

const PLAYER_SPRITE: &str = "player_a.png";

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
        .run();
}
