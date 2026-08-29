use bevy::{
    asset::AssetServer,
    camera::Camera2d,
    ecs::system::{Commands, Res},
};

use crate::plugins::shared::GameTexture;

pub fn spawn_camera(mut commands: Commands) {
    commands.spawn(Camera2d);
}

pub fn load_textures(mut commands: Commands, asset_server: Res<AssetServer>) {
    let background = asset_server.load("graphics/other/background.png");
    let ball = asset_server.load("graphics/other/ball.png");

    let game_texture = GameTexture { background, ball };

    commands.insert_resource(game_texture);
}
