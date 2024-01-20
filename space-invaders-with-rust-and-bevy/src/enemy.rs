use crate::{
    assets::{ENEMY_LASER_SIZE, ENEMY_SIZE, SPRITE_SCALE},
    components::{Enemy, Laser, LaserFromEnemy, Movable, SpriteSize, Velocity},
    resources::{EnemyCount, GameTextures, WindowSize, ENEMY_COUNT_MAX},
};
use bevy::prelude::{
    App, Commands, IntoSystemConfigs, Plugin, PostStartup, Quat, Query, Res, ResMut, SpriteBundle,
    Transform, Update, Vec3, With,
};
use bevy::time::common_conditions::on_timer;
use rand::{thread_rng, Rng};
use std::f32::consts::PI;
use std::time::Duration;

// Use enemy functionality as a plugin
pub struct EnemyPlugin;

impl Plugin for EnemyPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(PostStartup, enemy_spawn_system)
            .add_systems(
                Update,
                (
                    enemy_spawn_system.run_if(on_timer(Duration::from_secs(1))),
                    enemy_fire_system.run_if(on_timer(Duration::from_secs(1))),
                ),
            );
    }
}

fn enemy_spawn_system(
    mut commands: Commands,
    game_textures: Res<GameTextures>,
    mut enemy_count: ResMut<EnemyCount>,
    window_size: Res<WindowSize>,
) {
    if enemy_count.0 < ENEMY_COUNT_MAX {
        // compute random X and Y coordinates
        let mut random_generator = thread_rng();
        let width_span = window_size.width / 2. - 100.;
        let height_span = window_size.height / 2. - 100.;
        let x = random_generator.gen_range(-width_span..width_span);
        let y = random_generator.gen_range(-height_span..height_span);

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
