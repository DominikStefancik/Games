use bevy::{
    camera::visibility::Visibility,
    ecs::{
        observer::On,
        system::{Commands, Query, Res},
    },
    sprite::Sprite,
    transform::components::Transform,
};

use crate::plugins::{
    BoxTextureParts, Brick, BrickCollided, BrickType, Collider, GameInfo, GameTexture,
    calculate_brick_position, calculate_brick_size, spawn_box_texture_parts,
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

pub fn update_or_destroy_brick(
    trigger: On<BrickCollided>,
    mut commands: Commands,
    game_texture: Res<GameTexture>,
    mut brick_query: Query<&mut Brick>,
    box_texture_parts_query: Query<&BoxTextureParts>,
    mut sprite_query: Query<&mut Sprite>,
) {
    let BrickCollided { brick_entity } = trigger.event();

    // Get the Brick component out of given brick entity
    let Ok(mut brick) = brick_query.get_mut(*brick_entity) else {
        return;
    };
    // Get children representing image parts out of given brick entity
    let Ok(parts) = box_texture_parts_query.get(*brick_entity) else {
        return;
    };

    if brick.brick_type == BrickType::Blue {
        commands.entity(*brick_entity).despawn();
    } else {
        brick.update_type();
        let box_textures = game_texture.get_brick_texture(brick.brick_type);

        sprite_query.get_mut(parts.top_left).unwrap().image = box_textures.top_left;
        sprite_query.get_mut(parts.top).unwrap().image = box_textures.top;
        sprite_query.get_mut(parts.top_right).unwrap().image = box_textures.top_right;
        sprite_query.get_mut(parts.left).unwrap().image = box_textures.left;
        sprite_query.get_mut(parts.right).unwrap().image = box_textures.right;
        sprite_query.get_mut(parts.bottom_left).unwrap().image = box_textures.bottom_left;
        sprite_query.get_mut(parts.bottom).unwrap().image = box_textures.bottom;
        sprite_query.get_mut(parts.bottom_right).unwrap().image = box_textures.bottom_right;
        sprite_query.get_mut(parts.center).unwrap().image = box_textures.center;
    }
}
