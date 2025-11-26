use bevy::{
    app::{App, FixedUpdate, Startup},
    prelude::Plugin,
};

use crate::{
    main_menu::systems::spawn_main_text,
    scenes::systems::{
        scroll_background, scroll_platform, spawn_background, spawn_camera, spawn_platform,
    },
    sonic::systems::spawn_sonic,
};

mod systems;

pub struct MainMenuPlugin;

impl Plugin for MainMenuPlugin {
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
