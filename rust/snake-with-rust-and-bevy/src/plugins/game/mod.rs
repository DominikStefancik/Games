use bevy::{
    app::{App, Plugin, Update},
    state::{app::AppExtStates, state::OnEnter},
    time::{Timer, TimerMode},
};

mod events;
mod resources;
mod states;
mod systems;

pub use events::*;
pub use resources::*;
pub use states::*;
pub use systems::*;

use crate::plugins::shared::GAME_STARTING_INTERVAL;

pub struct GamePlugin;

impl Plugin for GamePlugin {
    fn build(&self, app: &mut App) {
        app.init_state::<GameState>()
            .insert_resource(GameStartingTimer(Timer::from_seconds(
                GAME_STARTING_INTERVAL,
                TimerMode::Once,
            )))
            /*
             * Commands don't mutate the World immediately — they queue up a command, and that queue is only applied ("flushed")
             * at a sync point (an apply_deferred call Bevy inserts into the schedule graph).
             * So the resource doesn't exist in the World the instant that line runs; it exists once the next sync point is reached.
             *
             * Practically, for Startup this means:
             *  - Bevy's startup sequence is actually three separate schedules run in order: PreStartup → Startup → PostStartup.
             *  - Bevy automatically flushes commands between schedules, so by the time PostStartup systems run (and certainly by
             *    the time the first Update runs), a resource is guaranteed to be inserted and available via
             *    Res<MyResource> / ResMut<MyResource>.
             *  - Within the same schedule, whether the resource is available to another system depends on ordering.
             *    If system B needs the resource inserted by system A, we need an explicit ordering (B.after(A)),
             *    and Bevy's automatic dependency-based sync insertion (auto_insert_apply_deferred, on by default)
             *    will insert a flush between them because it detects A writes deferred commands that B might depend on.
             *    Without ordering, A and B could run in parallel and B might not see the resource yet.
             *
             * If you just need the resource available for Update (or later) systems, "commands.insert_resource" in any
             * startup system is fine — it'll be flushed before Update starts.
             * If another Startup-stage system needs it in the same schedule, either order the systems explicitly (.after())
             * or just use "world.insert_resource" / a plain exclusive system for immediate insertion.
             */
            .add_systems(OnEnter(GameState::GameStarting), trigger_game_start)
            .add_systems(Update, move_to_playing_state)
            .add_observer(reset_game);
    }
}
