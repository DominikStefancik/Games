use bevy::{
    app::{App, FixedUpdate, PostStartup},
    ecs::schedule::IntoScheduleConfigs,
    prelude::Plugin,
    state::{
        condition::in_state,
        state::{OnEnter, OnExit},
    },
};

use crate::{
    app_states::AppState,
    game::GameState,
    sonic::systems::{
        despawn_sonic, detect_collision_sonic_with_ring, jump, reset_sonic_score_text, spawn_sonic,
        start_jump, trigger_jump,
    },
};

pub mod components;
pub mod events;
mod helpers;
pub mod systems;

pub struct SonicPlugin;

impl Plugin for SonicPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(PostStartup, spawn_sonic)
            .add_systems(OnEnter(AppState::Game), spawn_sonic)
            .add_systems(OnExit(AppState::MainMenu), despawn_sonic)
            .add_systems(OnExit(AppState::Game), despawn_sonic)
            .add_systems(
                FixedUpdate,
                (
                    detect_collision_sonic_with_ring,
                    trigger_jump,
                    jump.after(trigger_jump),
                    reset_sonic_score_text.after(detect_collision_sonic_with_ring),
                )
                    .run_if(in_state(AppState::Game))
                    .run_if(in_state(GameState::Running)),
            )
            // Global observers
            .add_observer(start_jump);
    }
}
