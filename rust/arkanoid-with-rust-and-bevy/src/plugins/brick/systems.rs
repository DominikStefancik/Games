use bevy::{
    color::Color,
    ecs::system::{Commands, Res},
    sprite::Sprite,
    transform::components::Transform,
};

use crate::plugins::{
    Brick, BrickType, Collider, GameTexture, LevelInfo, calculate_brick_position,
    calculate_brick_size,
};

pub fn spawn_bricks(
    mut commands: Commands,
    game_texture: Res<GameTexture>,
    level_info: Res<LevelInfo>,
) {
    for (row_index, row) in level_info.level_map.iter().enumerate() {
        let bricks_in_row_count = row.len() as u32;
        let brick_size = calculate_brick_size(bricks_in_row_count);

        for (character_index, character) in row.chars().enumerate() {
            if character.is_ascii_digit() {
                commands.spawn((
                    Sprite::from_color(Color::WHITE, brick_size),
                    Transform::from_translation(calculate_brick_position(
                        row_index,
                        character_index,
                        brick_size,
                    )),
                    Brick {
                        brick_type: BrickType::blue,
                    },
                    Collider { size: brick_size },
                ));
            }
        }
    }
}
