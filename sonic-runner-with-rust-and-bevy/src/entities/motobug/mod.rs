use bevy::{
    app::{App, FixedUpdate, Plugin},
    ecs::schedule::IntoScheduleConfigs,
    state::{condition::in_state, state::OnExit},
};

use crate::{
    app_states::AppState,
    entities::motobug::{
        resources::MotobugGenerationTimer,
        systems::{
            despawn_all_motobugs, despawn_motobug_out_of_screen, move_motobug, spawn_motobug,
        },
    },
    scenes::game::GameState,
};

pub struct MotobugPlugin;

pub mod components;
mod resources;
mod systems;

impl Plugin for MotobugPlugin {
    fn build(&self, app: &mut App) {
        app.insert_resource(MotobugGenerationTimer::new(0.7))
            .add_systems(OnExit(AppState::Game), despawn_all_motobugs)
            .add_systems(
                FixedUpdate,
                (spawn_motobug, move_motobug, despawn_motobug_out_of_screen)
                    .run_if(in_state(AppState::Game))
                    .run_if(in_state(GameState::Running)),
            );
    }
}
