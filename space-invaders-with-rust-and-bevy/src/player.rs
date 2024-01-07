use crate::assets::{PLAYER_SIZE, SPRITE_SCALE};
use crate::resources::{GameTextures, WindowSize};
use bevy::prelude::{App, Commands, Plugin, PostStartup, Res, SpriteBundle, Transform, Vec3};

// Use player functionality as a plugin
pub struct PlayerPlugin;

// Custom plugin in Bevy has to implement the trait "Plugin" in order to be able to be used
impl Plugin for PlayerPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(PostStartup, player_spawn_system);
    }
}

fn player_spawn_system(
    mut commands: Commands,
    game_textures: Res<GameTextures>,
    window_size: Res<WindowSize>,
) {
    // position the player at the bottom
    let bottom = -window_size.height / 2.;

    // Add the player
    commands.spawn(SpriteBundle {
        texture: game_textures.player.clone(),
        transform: Transform {
            translation: Vec3::new(
                0_f32,
                bottom + PLAYER_SIZE.1 / 2_f32 * SPRITE_SCALE + 5_f32,
                10_f32,
            ),
            scale: Vec3::new(SPRITE_SCALE, SPRITE_SCALE, 1.),
            ..Default::default()
        },
        ..Default::default()
    });
}
