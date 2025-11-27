use bevy::{
    app::{App, FixedUpdate},
    ecs::schedule::IntoScheduleConfigs,
    prelude::Plugin,
    state::{condition::in_state, state::OnExit},
};

use crate::{
    app_states::AppState,
    game::GameState,
    ring::{
        resources::RingGenerationTimer,
        systems::{despawn_all_rings, despawn_ring_out_of_screen, move_ring, spawn_ring},
    },
};

pub mod components;
pub mod resources;
pub mod systems;

pub struct RingPlugin;

impl Plugin for RingPlugin {
    fn build(&self, app: &mut App) {
        app.insert_resource(RingGenerationTimer::new(0.5))
            .add_systems(OnExit(AppState::Game), despawn_all_rings)
            .add_systems(
                FixedUpdate,
                (move_ring, despawn_ring_out_of_screen, spawn_ring)
                    .run_if(in_state(AppState::Game))
                    .run_if(in_state(GameState::Running)),
            );
    }
}
