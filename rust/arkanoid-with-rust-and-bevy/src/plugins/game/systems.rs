use bevy::{
    ecs::system::{Commands, Res},
    math::Vec3,
    sprite::Sprite,
    transform::components::Transform,
};

use crate::plugins::{WINDOW_RESOLUTION, shared::GameTexture};

const BACKGROUND_SPRITE_SIZE: (f32, f32) = (1204., 512.);

pub fn spawn_background(mut commands: Commands, game_texture: Res<GameTexture>) {
    commands.spawn((
        Sprite {
            image: game_texture.background.clone(),
            ..Default::default()
        },
        Transform::from_xyz(0., 0., 0.).with_scale(Vec3::new(
            WINDOW_RESOLUTION.0 as f32 / BACKGROUND_SPRITE_SIZE.0,
            WINDOW_RESOLUTION.1 as f32 / BACKGROUND_SPRITE_SIZE.1,
            1.,
        )),
    ));
}
