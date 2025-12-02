use bevy::{
    asset::{AssetServer, Assets},
    camera::Camera2d,
    ecs::system::{Commands, Res, ResMut},
    image::TextureAtlasLayout,
    math::UVec2,
};

use crate::{
    resources::{GameFonts, GameSounds, GameTextures},
    ring::components::RING_SPRITE_FRAME_SIZE,
    sonic::components::SONIC_SPRITE_FRAME_SIZE,
};

pub fn spawn_camera(mut commands: Commands) {
    commands.spawn(Camera2d);
}

pub fn load_textures(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
    mut texture_atlas_layouts: ResMut<Assets<TextureAtlasLayout>>,
) {
    let background = asset_server.load("graphics/chemical-background.png");
    let platforms = asset_server.load("graphics/platforms.png");

    // create sonic texture atlas
    let sonic = asset_server.load("graphics/sonic.png");
    let layout = TextureAtlasLayout::from_grid(
        UVec2::new(
            SONIC_SPRITE_FRAME_SIZE.0 as u32,
            SONIC_SPRITE_FRAME_SIZE.1 as u32,
        ),
        8,
        2,
        None,
        None,
    );
    let sonic_atlas = texture_atlas_layouts.add(layout);

    // create ring texture atlas
    let ring = asset_server.load("graphics/ring.png");
    let layout = TextureAtlasLayout::from_grid(
        UVec2::new(
            RING_SPRITE_FRAME_SIZE.0 as u32,
            RING_SPRITE_FRAME_SIZE.1 as u32,
        ),
        16,
        1,
        None,
        None,
    );
    let ring_atlas = texture_atlas_layouts.add(layout);

    let game_textures = GameTextures {
        background,
        platforms,
        sonic,
        sonic_atlas,
        ring,
        ring_atlas,
    };

    commands.insert_resource(game_textures);
}

pub fn load_sounds(mut commands: Commands, asset_server: Res<AssetServer>) {
    let background = asset_server.load("sounds/City.mp3");
    let ring = asset_server.load("sounds/Ring.wav");
    let jump = asset_server.load("sounds/Jump.wav");

    let game_sounds = GameSounds {
        background,
        ring,
        jump,
    };

    commands.insert_resource(game_sounds);
}

pub fn load_fonts(mut commands: Commands, asset_server: Res<AssetServer>) {
    let mania = asset_server.load("fonts/mania.ttf");

    let game_fonts = GameFonts { mania };

    commands.insert_resource(game_fonts);
}
