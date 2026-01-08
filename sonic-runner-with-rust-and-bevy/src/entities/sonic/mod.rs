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
    entities::sonic::systems::{
        despawn_sonic, detect_collision_sonic_with_motobug, detect_collision_sonic_with_ring, jump,
        reset_sonic_score_text, spawn_sonic, start_jump, trigger_jump,
    },
    scenes::game::GameState,
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
                    (
                        detect_collision_sonic_with_ring,
                        detect_collision_sonic_with_motobug,
                    )
                        .before(reset_sonic_score_text),
                    trigger_jump,
                    jump.after(trigger_jump),
                    reset_sonic_score_text,
                )
                    .run_if(in_state(AppState::Game))
                    .run_if(in_state(GameState::Running)),
            )
            // Global observers
            .add_observer(start_jump);
    }
}
