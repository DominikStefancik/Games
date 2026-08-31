use bevy::{
    ecs::system::{Commands, Res},
    math::{Vec2, Vec3},
    sprite::Sprite,
    transform::components::Transform,
};

use crate::plugins::{
    GameTexture, HEART_SIDE_OFFSET, HEART_TEXTURE_SIZE, HEART_TOP_OFFSET, HEARTS_GAP, Heart,
    LevelInfo, WINDOW_RESOLUTION, WINDOW_RESOLUTION_HALF,
};

const BACKGROUND_SPRITE_SIZE: Vec2 = Vec2::new(1204., 512.);

pub fn spawn_background(mut commands: Commands, game_texture: Res<GameTexture>) {
    commands.spawn((
        Sprite {
            image: game_texture.background.clone(),
            ..Default::default()
        },
        Transform::from_xyz(0., 0., 0.).with_scale(Vec3::new(
            WINDOW_RESOLUTION.0 as f32 / BACKGROUND_SPRITE_SIZE.x,
            WINDOW_RESOLUTION.1 as f32 / BACKGROUND_SPRITE_SIZE.y,
            1.,
        )),
    ));
}

pub fn spawn_hearts(
    mut commands: Commands,
    game_texture: Res<GameTexture>,
    game_info: Res<LevelInfo>,
) {
    for index in 0..game_info.lives {
        let position = Vec2::new(
            -WINDOW_RESOLUTION_HALF.x
                + HEART_SIDE_OFFSET
                + index as f32 * (HEART_TEXTURE_SIZE.x + HEARTS_GAP)
                + HEART_TEXTURE_SIZE.x / 2.,
            WINDOW_RESOLUTION_HALF.y - HEART_TEXTURE_SIZE.y / 2. - HEART_TOP_OFFSET,
        );

        commands.spawn((
            Sprite {
                image: game_texture.heart.clone(),
                ..Default::default()
            },
            Transform::from_translation(position.extend(1.)),
            Heart { index },
        ));
    }
}
