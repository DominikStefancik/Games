use std::collections::HashSet;

use bevy::{
    camera::visibility::Visibility,
    ecs::{
        entity::Entity,
        observer::On,
        query::With,
        system::{Commands, Query, Res, Single},
    },
    math::bounding::Aabb2d,
    sprite::Sprite,
    transform::components::Transform,
};

use crate::plugins::{
    Brick, BrickDestroyed, Collider, GameTexture, INITIAL_PADDLE_SIZE, LASER_MAX_COUNT,
    LASER_TEXTURE_SIZE, LASER_VERTICAL_OFFSET, Laser, LaserUpgradeDestroyed, PADDLE_MOVEMENT_SPEED,
    PROJECTILE_MOVEMENT_SPEED, PROJECTILE_TEXTURE_SIZE, Paddle, Projectile, ProjectileShot,
    WINDOW_RESOLUTION_HALF, detect_rectangle_collision, get_laser_horizontal_position,
    get_paddle_initial_position, spawn_box_texture_parts,
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

pub fn spawn_laser(
    _: On<LaserUpgradeDestroyed>,
    mut commands: Commands,
    game_texture: Res<GameTexture>,
    paddle_query: Single<(Entity, &mut Paddle)>,
) {
    let (entity, mut paddle) = paddle_query.into_inner();

    if paddle.laser_count < LASER_MAX_COUNT {
        let laser = commands
            .spawn((
                Sprite {
                    image: game_texture.laser.clone(),
                    ..Default::default()
                },
                Transform::from_xyz(0., paddle.size.y - LASER_VERTICAL_OFFSET, 1.),
                Laser,
            ))
            .id();

        commands.entity(entity).add_child(laser);

        paddle.laser_count += 1;
    }
}

pub fn adjust_lasers_position(
    paddle: Single<&Paddle>,
    mut laser_query: Query<&mut Transform, With<Laser>>,
) {
    for (index, mut transform) in laser_query.iter_mut().enumerate() {
        transform.translation.x =
            get_laser_horizontal_position(paddle.size.x / 2., paddle.laser_count, index);
    }
}

pub fn spawn_projectiles(
    _: On<ProjectileShot>,
    mut commands: Commands,
    game_texture: Res<GameTexture>,
    paddle_query: Single<&Transform, With<Paddle>>,
    laser_query: Query<&Transform, With<Laser>>,
) {
    let paddle_transform = paddle_query.into_inner();

    for laser_transform in laser_query {
        let mut projectile_position = paddle_transform.translation + laser_transform.translation;
        projectile_position.y += LASER_TEXTURE_SIZE.y;

        commands.spawn((
            Sprite {
                image: game_texture.projectile.clone(),
                ..Default::default()
            },
            Transform::from_translation(projectile_position),
            Projectile,
        ));
    }
}

pub fn move_projectile(
    mut commands: Commands,
    query: Query<(Entity, &mut Transform), With<Projectile>>,
) {
    for (entity, mut transform) in query {
        transform.translation.y += PROJECTILE_MOVEMENT_SPEED;

        if transform.translation.y >= WINDOW_RESOLUTION_HALF.y - PROJECTILE_TEXTURE_SIZE.y / 2. {
            commands.entity(entity).despawn();
        }
    }
}

pub fn check_projectile_collision(
    mut commands: Commands,
    projectile_query: Query<(Entity, &Transform), With<Projectile>>,
    collider_query: Query<(Entity, &Transform, &Collider, Option<&Brick>)>,
) {
    let mut despawned_projectiles: HashSet<Entity> = HashSet::new();
    let mut despawned_bricks: HashSet<Entity> = HashSet::new();

    /*
     * Our loop structure is nested: for every brick collider, we check every projectile. If a single projectile
     * happens to overlap two bricks in the same frame (e.g. two adjacent bricks), we'll queue
     * "commands.entity(projectile_entity).despawn()" twice — once per collider it matched against.
     * Same risk in reverse: if two projectiles hit the same brick in the same frame, we queue
     * "commands.entity(collider_entity).despawn()" twice for that brick. The second despawn in either case
     * is the one throwing the warning, unless we keep track what was already despawned.
     * To fix this we need to track what's already been despawned this frame, and stop checking it again.
     */
    for (collider_entity, collider_transform, collider, optional_brick) in collider_query {
        if despawned_bricks.contains(&collider_entity) {
            continue; // this brick is already destroyed this frame, skip it
        }

        for (projectile_entity, projectile_transform) in projectile_query {
            if despawned_projectiles.contains(&projectile_entity) {
                continue; // this projectile already hit something else this frame
            }

            let is_colliding = detect_rectangle_collision(
                Aabb2d::new(
                    projectile_transform.translation.truncate(),
                    PROJECTILE_TEXTURE_SIZE / 2.,
                ),
                Aabb2d::new(
                    collider_transform.translation.truncate(),
                    collider.size / 2.,
                ),
            );

            if is_colliding && optional_brick.is_some() {
                commands.trigger(BrickDestroyed {
                    brick_position: collider_transform.translation,
                });
                commands.entity(collider_entity).despawn();
                commands.entity(projectile_entity).despawn();

                despawned_bricks.insert(collider_entity);
                despawned_projectiles.insert(projectile_entity);

                break; // this projectile is spent — no point checking it against more bricks
            }
        }
    }
}
