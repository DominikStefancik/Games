use bevy::{
    camera::visibility::Visibility,
    ecs::{
        observer::On,
        system::{Commands, Res, Single},
    },
    state::state::State,
    transform::components::Transform,
};

use crate::plugins::{
    BOTTOM_OFFSET, Collider, GameState, GameTexture, INITIAL_PADDLE_SIZE, LaserUpgradeDestroyed,
    PADDLE_MOVEMENT_SPEED, Paddle, WINDOW_RESOLUTION_HALF, is_game_starting_or_running,
    spawn_box_texture_parts,
};

pub fn spawn_paddle(mut commands: Commands, game_texture: Res<GameTexture>) {
    let mut parts = None;

    let parent_entity = commands
        .spawn((
            Transform::from_xyz(0., -WINDOW_RESOLUTION_HALF.y + BOTTOM_OFFSET, 1.),
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

pub fn move_paddle(
    app_state: Res<State<GameState>>,
    paddle_query: Single<(&mut Transform, &Paddle)>,
) {
    if !is_game_starting_or_running(app_state.get()) {
        return;
    }

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

pub fn spawn_laser(
    _: On<LaserUpgradeDestroyed>,
    mut commands: Commands,
    game_texture: Res<GameTexture>,
) {
}
