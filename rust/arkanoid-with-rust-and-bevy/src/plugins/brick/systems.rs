use bevy::{
    camera::visibility::Visibility,
    ecs::system::{Commands, Res},
    transform::components::Transform,
};

use crate::plugins::{
    Brick, BrickType, Collider, GameInfo, GameTexture, calculate_brick_position,
    calculate_brick_size, spawn_box_texture_parts,
};

pub fn spawn_bricks(
    mut commands: Commands,
    game_texture: Res<GameTexture>,
    game_info: Res<GameInfo>,
) {
    for (row_index, row) in game_info.level_map.iter().enumerate() {
        let bricks_in_row_count = row.len() as f32;
        let brick_size = calculate_brick_size(bricks_in_row_count);

        for (character_index, character) in row.chars().enumerate() {
            if character.is_ascii_digit() {
                let brick_type = BrickType::from(character.to_string().as_str());
                let mut parts = None;

                let parent_entity = commands
                    .spawn((
                        /*
                         * Sprite requires (and auto-inserts) GlobalTransform, InheritedVisibility, and ViewVisibility
                         * on any entity it's attached to. Those are "hierarchy-inherited" components — they get computed
                         * by walking up the parent chain each frame. If a child has Transform or Visibility
                         * but its parent doesn't, Bevy can't propagate the value correctly and we get a warning.
                         */
                        Transform::from_translation(calculate_brick_position(
                            row_index,
                            character_index,
                            brick_size,
                        )),
                        Visibility::default(), // required so InheritedVisibility propagates correctly
                        Brick { brick_type },
                        Collider { size: brick_size },
                    ))
                    .with_children(|parent_sprite| {
                        parts = spawn_box_texture_parts(
                            parent_sprite,
                            &game_texture.get_brick_texture(brick_type),
                        );
                    })
                    .id();

                /* Note: parts is populated by the time `with_children` returns,
                 * since the closure runs synchronously — but the entities are only
                 * created when commands are flushed. Insert it as a separate component
                 * */
                commands.entity(parent_entity).insert(parts.unwrap());
            }
        }
    }
}
