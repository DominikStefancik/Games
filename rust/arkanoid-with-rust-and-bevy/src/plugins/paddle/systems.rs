use bevy::{
    camera::visibility::Visibility,
    ecs::{
        observer::On,
        system::{Commands, Res, Single},
    },
    sprite::Sprite,
    transform::components::Transform,
};

use crate::plugins::{
    BOTTOM_OFFSET, Collider, GameTexture, HALF_PADDLE, LaserUpgradeDestroyed,
    PADDLE_MOVEMENT_SPEED, PADDLE_SIZE, Paddle, SizeUpgradeDestroyed, WINDOW_RESOLUTION_HALF,
    spawn_box_texture_parts,
};

pub fn spawn_paddle(mut commands: Commands, game_texture: Res<GameTexture>) {
    let mut parts = None;

    let parent_entity = commands
        .spawn((
            Transform::from_xyz(0., -WINDOW_RESOLUTION_HALF.y + BOTTOM_OFFSET, 1.),
            Visibility::default(), // required so InheritedVisibility propagates correctly
            Paddle {
                size: PADDLE_SIZE,
                direction: 0.,
                speed: PADDLE_MOVEMENT_SPEED,
                laser_count: 0,
            },
            Collider { size: PADDLE_SIZE },
        ))
        .with_children(|parent_sprite| {
            parts = spawn_box_texture_parts(parent_sprite, &game_texture.paddle, PADDLE_SIZE);
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

    transform.translation.x += paddle.direction * paddle.speed;

    let left_border = -WINDOW_RESOLUTION_HALF.x;
    let right_border = WINDOW_RESOLUTION_HALF.x;

    if transform.translation.x - HALF_PADDLE <= left_border {
        transform.translation.x = left_border + HALF_PADDLE;
    }

    if transform.translation.x + HALF_PADDLE >= right_border {
        transform.translation.x = right_border - HALF_PADDLE
    }
}

pub fn spawn_new_laser(
    _: On<LaserUpgradeDestroyed>,
    mut commands: Commands,
    game_texture: Res<GameTexture>,
) {
}

pub fn resize_paddle(_: On<SizeUpgradeDestroyed>, paddle_query: Single<(&mut Sprite, &Paddle)>) {}
