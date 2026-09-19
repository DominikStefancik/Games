use bevy::{
    ecs::system::Commands,
    math::{Vec2, Vec3},
    sprite::Sprite,
    transform::components::Transform,
};

use crate::plugins::{
    GameTexture, HEART_SCALE, HEART_SIDE_OFFSET, HEART_TEXTURE_SIZE, HEART_TOP_OFFSET, HEARTS_GAP,
    Heart, WINDOW_RESOLUTION_HALF,
};

pub fn calculate_heart_horizontal_position(index: u16) -> f32 {
    WINDOW_RESOLUTION_HALF.x
        - HEART_SIDE_OFFSET
        - index as f32 * (HEART_TEXTURE_SIZE.x + HEARTS_GAP)
        - HEART_TEXTURE_SIZE.x / 2.
}

pub fn spawn_all_hearts(commands: &mut Commands, game_texture: &GameTexture, lives: u16) {
    for index in 0..lives {
        spawn_single_heart(commands, game_texture, index);
    }
}

pub fn spawn_single_heart(commands: &mut Commands, game_texture: &GameTexture, index: u16) {
    let position = Vec2::new(
        calculate_heart_horizontal_position(index),
        WINDOW_RESOLUTION_HALF.y - HEART_TEXTURE_SIZE.y / 2. - HEART_TOP_OFFSET,
    );

    commands.spawn((
        Sprite {
            image: game_texture.heart.clone(),
            ..Default::default()
        },
        Transform::from_translation(position.extend(1.)).with_scale(Vec3::splat(HEART_SCALE)),
        Heart { index },
    ));
}
