use bevy::{
    app::{App, FixedUpdate, Startup},
    prelude::Plugin,
    state::{app::AppExtStates, state::States},
};

use crate::{
    game::systems::toggle_pausing_game,
    scenes::systems::{scroll_background, scroll_platform, spawn_background, spawn_platform},
    sonic::systems::spawn_sonic,
};

mod systems;

pub struct GamePlugin;

#[derive(States, Debug, Clone, Copy, Eq, PartialEq, Hash, Default)]
pub enum GameState {
    // this says Running will be a default state of the game when we move to the Game state in our app
    #[default]
    Running,
    Paused,
}

impl Plugin for GamePlugin {
    fn build(&self, app: &mut App) {
        app.init_state::<GameState>() // Alternatively we could use .insert_state(GameState::Running)
            .add_systems(Startup, (spawn_background, spawn_platform, spawn_sonic))
            .add_systems(
                FixedUpdate,
                (scroll_background, scroll_platform, toggle_pausing_game),
            );
    }
}
