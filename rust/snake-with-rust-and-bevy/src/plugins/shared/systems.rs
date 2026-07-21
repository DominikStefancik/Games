use bevy::ecs::system::Commands;

use crate::plugins::shared::events::GameStarted;

pub fn initialise_game(mut commands: Commands) {
    commands.trigger(GameStarted());
}
