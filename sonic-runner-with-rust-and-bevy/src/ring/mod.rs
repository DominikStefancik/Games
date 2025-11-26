use bevy::{
    app::{App, FixedUpdate},
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
    ring::systems::{despawn_all_rings, despawn_ring_out_of_screen, move_ring, spawn_ring},
};

pub mod components;
pub mod systems;

pub struct RingPlugin;

impl Plugin for RingPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(OnEnter(AppState::Game), spawn_ring)
            .add_systems(OnExit(AppState::Game), despawn_all_rings)
            .add_systems(
                FixedUpdate,
                (move_ring, despawn_ring_out_of_screen)
                    .run_if(in_state(AppState::Game))
                    .run_if(in_state(GameState::Running)),
            );
    }
}
