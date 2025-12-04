use bevy::{
    app::{App, FixedUpdate, PostStartup},
    ecs::schedule::IntoScheduleConfigs,
    prelude::Plugin,
    state::{condition::in_state, state::OnExit},
};

use crate::{
    app_states::AppState,
    scenes::{
        main_menu::systems::{despawn_main_text, spawn_main_text},
        systems::{
            despawn_backgrounds, despawn_platforms, scroll_background, scroll_platform,
            spawn_background, spawn_platform,
        },
    },
};

mod components;
mod systems;

pub struct MainMenuPlugin;

impl Plugin for MainMenuPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(
            PostStartup,
            (spawn_background, spawn_platform, spawn_main_text),
        )
        .add_systems(
            FixedUpdate,
            (
                scroll_background.run_if(in_state(AppState::MainMenu)),
                scroll_platform.run_if(in_state(AppState::MainMenu)),
            ),
        )
        .add_systems(
            OnExit(AppState::MainMenu),
            (despawn_backgrounds, despawn_platforms, despawn_main_text),
        );
    }
}
