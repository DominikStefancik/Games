use bevy::{
    asset::AssetServer,
    ecs::system::{Commands, Res},
};

use crate::plugins::shared::GameSounds;

pub fn load_sounds(mut commands: Commands, asset_server: Res<AssetServer>) {
    let eat = asset_server.load("audio/eat.wav");
    let die = asset_server.load("audio/die.wav");

    let game_sounds = GameSounds { eat, die };

    commands.insert_resource(game_sounds);
}
