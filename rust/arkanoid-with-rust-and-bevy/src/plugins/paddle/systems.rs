use bevy::{
    camera::visibility::Visibility,
    ecs::system::{Commands, Res, Single},
    transform::components::Transform,
};

use crate::plugins::{
    Collider, GameTexture, INITIAL_PADDLE_SIZE, PADDLE_MOVEMENT_SPEED, Paddle,
    WINDOW_RESOLUTION_HALF, get_paddle_initial_position, spawn_box_texture_parts,
};

pub fn spawn_paddle(mut commands: Commands, game_texture: Res<GameTexture>) {
    let mut parts = None;

    let parent_entity = commands
        .spawn((
            Transform::from_translation(get_paddle_initial_position()),
            Visibility::default(), // required so InheritedVisibility propagates correctly
            Paddle {
                size: INITIAL_PADDLE_SIZE,
                direction: 0.,
                speed: PADDLE_MOVEMENT_SPEED,
                laser_count: 0,
            },
            Collider {
                size: INITIAL_PADDLE_SIZE,
            },
        ))
        .with_children(|parent_sprite| {
            parts = spawn_box_texture_parts(parent_sprite, &game_texture.paddle);
        })
        .id();

    /* Note: parts is populated by the time `with_children` returns,
     * since the closure runs synchronously — but the entities are only
     * created when commands are flushed. Insert it as a separate component:
     * */
    commands.entity(parent_entity).insert(parts.unwrap());
}

pub fn move_paddle(paddle_query: Single<(&mut Transform, &Paddle)>) {
    let (mut transform, paddle) = paddle_query.into_inner();
    let paddle_half_size = paddle.size / 2.;

    transform.translation.x += paddle.direction * paddle.speed;

    let left_border = -WINDOW_RESOLUTION_HALF.x;
    let right_border = WINDOW_RESOLUTION_HALF.x;

    if transform.translation.x - paddle_half_size.x <= left_border {
        transform.translation.x = left_border + paddle_half_size.x;
    }

    if transform.translation.x + paddle_half_size.x >= right_border {
        transform.translation.x = right_border - paddle_half_size.x
    }
}
