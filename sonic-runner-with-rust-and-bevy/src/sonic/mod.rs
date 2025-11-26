use bevy::{
    app::{App, FixedUpdate},
    prelude::Plugin,
    state::state::{OnEnter, OnExit},
};

use crate::{
    app_states::AppState,
    sonic::systems::{despawn_sonic, detect_collision_sonic_with_ring, spawn_sonic},
};

pub mod components;
pub mod systems;

pub struct SonicPlugin;

impl Plugin for SonicPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(OnEnter(AppState::MainMenu), spawn_sonic)
            .add_systems(OnEnter(AppState::Game), spawn_sonic)
            .add_systems(OnExit(AppState::MainMenu), despawn_sonic)
            .add_systems(OnExit(AppState::Game), despawn_sonic)
            .add_systems(FixedUpdate, detect_collision_sonic_with_ring);
    }
}
