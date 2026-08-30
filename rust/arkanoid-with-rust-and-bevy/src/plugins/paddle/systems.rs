use bevy::{
    camera::visibility::Visibility,
    ecs::system::{Commands, Res, Single},
    transform::components::Transform,
};

use crate::plugins::{
    BOTTOM_OFFSET, Collider, GameTexture, HALF_PADDLE, PADDLE_MOVEMENT_SPEED, PADDLE_SIZE, Paddle,
    WINDOW_RESOLUTION, spawn_box_texture_parts,
};

pub fn spawn_paddle(mut commands: Commands, game_texture: Res<GameTexture>) {
    commands
        .spawn((
            Transform::from_xyz(0., -((WINDOW_RESOLUTION.1 / 2 - BOTTOM_OFFSET) as f32), 1.),
            Visibility::default(), // required so InheritedVisibility propagates correctly
            Paddle {
                direction: 0.,
                speed: PADDLE_MOVEMENT_SPEED,
            },
            Collider { size: PADDLE_SIZE },
        ))
        .with_children(|parent_sprite| {
            spawn_box_texture_parts(parent_sprite, &game_texture.paddle, PADDLE_SIZE)
        });
}

pub fn move_paddle(paddle_query: Single<(&mut Transform, &Paddle)>) {
    let (mut transform, paddle) = paddle_query.into_inner();

    transform.translation.x += paddle.direction * paddle.speed;

    let left_border = -((WINDOW_RESOLUTION.0 / 2) as f32);
    let right_border = (WINDOW_RESOLUTION.0 / 2) as f32;

    if transform.translation.x - HALF_PADDLE <= left_border {
        transform.translation.x = left_border + HALF_PADDLE;
    }

    if transform.translation.x + HALF_PADDLE >= right_border {
        transform.translation.x = right_border - HALF_PADDLE
    }
}
