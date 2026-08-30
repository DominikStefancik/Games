use bevy::{
    asset::AssetServer,
    camera::Camera2d,
    ecs::system::{Commands, Res},
};

use crate::plugins::{load_box_graphics, shared::GameTexture};

pub fn spawn_camera(mut commands: Commands) {
    commands.spawn(Camera2d);
}

pub fn load_textures(mut commands: Commands, asset_server: Res<AssetServer>) {
    let background = asset_server.load("graphics/other/background.png");
    let ball = asset_server.load("graphics/other/ball.png");
    let paddle = load_box_graphics(&asset_server, "graphics/paddle");
    let blue_brick = load_box_graphics(&asset_server, "graphics/bricks/blue");
    let bronze_brick = load_box_graphics(&asset_server, "graphics/bricks/bronze");
    let green_brick = load_box_graphics(&asset_server, "graphics/bricks/green");
    let grey_brick = load_box_graphics(&asset_server, "graphics/bricks/grey");
    let orange_brick = load_box_graphics(&asset_server, "graphics/bricks/orange");
    let purple_brick = load_box_graphics(&asset_server, "graphics/bricks/purple");
    let red_brick = load_box_graphics(&asset_server, "graphics/bricks/red");
    let heart = asset_server.load("graphics/other/heart.png");

    let game_texture = GameTexture {
        background,
        ball,
        paddle,
        blue_brick,
        bronze_brick,
        green_brick,
        grey_brick,
        orange_brick,
        purple_brick,
        red_brick,
        heart,
    };

    commands.insert_resource(game_texture);
}
