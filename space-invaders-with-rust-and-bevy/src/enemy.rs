use crate::{
    assets::{ENEMY_SIZE, SPRITE_SCALE},
    components::{Enemy, SpriteSize},
    resources::{EnemyCount, GameTextures, WindowSize, ENEMY_COUNT_MAX},
};
use bevy::prelude::{
    App, Commands, IntoSystemConfigs, Plugin, PostStartup, Res, ResMut, SpriteBundle, Transform,
    Update, Vec3,
};
use bevy::time::common_conditions::on_timer;
use rand::{thread_rng, Rng};
use std::time::Duration;

// Use enemy functionality as a plugin
pub struct EnemyPlugin;

impl Plugin for EnemyPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(PostStartup, enemy_spawn_system)
            .add_systems(
                Update,
                enemy_spawn_system.run_if(on_timer(Duration::from_secs(1))),
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
