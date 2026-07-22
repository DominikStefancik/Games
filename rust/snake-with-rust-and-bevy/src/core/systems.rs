use bevy::{
    asset::AssetServer,
    ecs::system::{Commands, Res},
};

use crate::core::{GameFonts, GameSounds};

pub fn load_fonts(mut commands: Commands, asset_server: Res<AssetServer>) {
    let bebas_neue_regular = asset_server.load("fonts/BebasNeue-Regular.ttf");

    let game_fonts = GameFonts { bebas_neue_regular };

    commands.insert_resource(game_fonts);
}

pub fn load_sounds(mut commands: Commands, asset_server: Res<AssetServer>) {
    let eat = asset_server.load("audio/eat.wav");

    let game_sounds = GameSounds { eat };

    commands.insert_resource(game_sounds);
}
