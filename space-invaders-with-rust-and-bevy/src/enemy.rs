use crate::{
    assets::{ENEMY_SIZE, SPRITE_SCALE},
    components::{Enemy, SpriteSize},
    resources::{GameTextures, WindowSize},
};
use bevy::prelude::{App, Commands, Plugin, PostStartup, Res, SpriteBundle, Transform, Vec3};
use rand::{thread_rng, Rng};

// Use enemy functionality as a plugin
pub struct EnemyPlugin;

impl Plugin for EnemyPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(PostStartup, enemy_spawn_system);
    }
}

fn enemy_spawn_system(
    mut commands: Commands,
    game_textures: Res<GameTextures>,
    window_size: Res<WindowSize>,
) {
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
}
