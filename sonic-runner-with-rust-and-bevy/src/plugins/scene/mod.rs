use bevy::{
    app::{App, FixedUpdate, Startup},
    prelude::Plugin,
};

use crate::{
    entities::sonic::systems::spawn_sonic,
    plugins::scene::systems::{
        scroll_background, scroll_platform, spawn_background, spawn_camera, spawn_main_text,
        spawn_platform,
    },
};

mod components;
mod systems;

pub struct ScenePlugin;

impl Plugin for ScenePlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(
            Startup,
            (
                spawn_camera,
                spawn_background,
                spawn_platform,
                spawn_sonic,
                spawn_main_text,
            ),
        )
        .add_systems(FixedUpdate, (scroll_background, scroll_platform));
    }
}
