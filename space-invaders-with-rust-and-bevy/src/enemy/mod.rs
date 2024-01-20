mod formation;

use crate::{
    assets::{ENEMY_LASER_SIZE, ENEMY_SIZE, SPRITE_SCALE, TIME_STEP},
    components::{Enemy, Laser, LaserFromEnemy, Movable, SpriteSize, Velocity},
    enemy::formation::{Formation, FormationFactory},
    resources::{EnemyCount, GameTextures, WindowSize, ENEMY_COUNT_MAX},
};
use bevy::prelude::{
    App, Commands, IntoSystemConfigs, Plugin, PostStartup, Quat, Query, Res, ResMut, SpriteBundle,
    Transform, Update, Vec3, With,
};
use bevy::time::common_conditions::on_timer;
use std::f32::consts::PI;
use std::time::Duration;

// Use enemy functionality as a plugin
pub struct EnemyPlugin;

impl Plugin for EnemyPlugin {
    fn build(&self, app: &mut App) {
        app.insert_resource(FormationFactory::default())
            .add_systems(PostStartup, enemy_spawn_system)
            .add_systems(
                Update,
                (
                    enemy_spawn_system.run_if(on_timer(Duration::from_secs(1))),
                    enemy_fire_system.run_if(on_timer(Duration::from_secs(1))),
                    enemy_movement_system,
                ),
            );
    }
}

fn enemy_spawn_system(
    mut commands: Commands,
    game_textures: Res<GameTextures>,
    mut enemy_count: ResMut<EnemyCount>,
    mut formation_factory: ResMut<FormationFactory>,
    window_size: Res<WindowSize>,
) {
    if enemy_count.0 < ENEMY_COUNT_MAX {
        // get formation and start point
        let formation = formation_factory.create_formation(&window_size);
        let (x, y) = formation.start_coordinate;

        commands
            .spawn(SpriteBundle {
                texture: game_textures.enemy.clone(),
                transform: Transform {
                    translation: Vec3::new(x, y, 10.),
                    scale: Vec3::new(SPRITE_SCALE, SPRITE_SCALE, 0.),
                    ..Default::default()
                },
                ..Default::default()
            })
            .insert(Enemy)
            .insert(formation)
            .insert(SpriteSize::from(ENEMY_SIZE));

        enemy_count.0 += 1;
    }
}

fn enemy_fire_system(
    mut commands: Commands,
    game_textures: Res<GameTextures>,
    // position of the enemy so we know where the position of its laser will be
    enemy_query: Query<&Transform, With<Enemy>>,
) {
    for &transform in enemy_query.iter() {
        let (x, y) = (transform.translation.x, transform.translation.y);
        // spawn enemy laser sprite
        commands
            .spawn(SpriteBundle {
                texture: game_textures.enemy_laser.clone(),
                transform: Transform {
                    translation: Vec3::new(x, y - 20., 0.),
                    rotation: Quat::from_rotation_x(PI),
                    scale: Vec3::new(SPRITE_SCALE, SPRITE_SCALE, 1.),
                    ..Default::default()
                },
                ..Default::default()
            })
            .insert(Laser)
            .insert(SpriteSize::from(ENEMY_LASER_SIZE))
            .insert(LaserFromEnemy)
            .insert(Movable { auto_despawn: true })
            .insert(Velocity { x: 0., y: -1. });
    }
}

fn enemy_movement_system(mut query: Query<(&mut Transform, &mut Formation), With<Enemy>>) {
    for (mut enemy_transform, mut formation) in query.iter_mut() {
        // get current position of the enemy
        let (current_position_x, current_position_y) =
            (enemy_transform.translation.x, enemy_transform.translation.y);

        // compute maximum distance of the movement
        let max_distance = TIME_STEP * formation.speed;

        // fixtures

        // 1 is clockwise, -1 is counter clockwise
        let direction: f32 = if formation.start_coordinate.0 < 0. {
            1.
        } else {
            -1.
        };
        let (ellipse_center_x, ellipse_center_y) = formation.pivot;
        let (ellipse_radius_x, ellipse_radius_y) = formation.radius;

        // compute next angle
        let angle = formation.angle
            + direction * formation.speed * TIME_STEP
                / (ellipse_radius_x.min(ellipse_radius_y) * PI / 2.);

        // compute target coordinates
        let destination_x = ellipse_radius_x * angle.cos() + ellipse_center_x;
        let destination_y = ellipse_radius_y * angle.sin() + ellipse_center_y;

        // compute distance
        let delta_x = current_position_x - destination_x;
        let delta_y = current_position_y - destination_y;
        let distance = (delta_x * delta_x + delta_y * delta_y).sqrt();
        let distance_ratio = if distance != 0. {
            max_distance / distance
        } else {
            0.
        };

        // compute final coordinates
        let x = current_position_x - delta_x * distance_ratio;
        let x = if delta_x > 0. {
            x.max(destination_x)
        } else {
            x.min(destination_x)
        };
        let y = current_position_y - delta_y * distance_ratio;
        let y = if delta_y > 0. {
            y.max(destination_y)
        } else {
            y.min(destination_y)
        };

        // start rotating the formation angle only when the sprite is on or close to the ellipse
        if distance < max_distance * formation.speed / 20. {
            formation.angle = angle;
        }

        let translation = &mut enemy_transform.translation;
        (translation.x, translation.y) = (x, y);
    }
}
