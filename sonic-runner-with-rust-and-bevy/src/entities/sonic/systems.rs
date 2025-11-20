use bevy::{
    asset::{AssetServer, Assets},
    ecs::system::{Commands, Res, ResMut},
    image::{TextureAtlas, TextureAtlasLayout},
    math::{UVec2, Vec3},
    sprite::Sprite,
    time::{Timer, TimerMode},
    transform::components::Transform,
};

use crate::{
    entities::components::{Animation, AnimationTimer},
    plugins::default::WINDOW_RESOLUTION,
};

const SONIC_SPRITE_SCALE: f32 = 3.;

pub fn spawn_sonic(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
    mut texture_atlas_layouts: ResMut<Assets<TextureAtlasLayout>>,
) {
    let texture = asset_server.load("graphics/sonic.png");
    let layout = TextureAtlasLayout::from_grid(UVec2::new(32, 44), 8, 2, None, None);
    let texture_atlas_layout = texture_atlas_layouts.add(layout);

    let run_animation = Animation {
        first_frame: 0,
        last_frame: 7,
    };

    commands.spawn((
        Sprite::from_atlas_image(
            texture.clone(),
            TextureAtlas {
                layout: texture_atlas_layout.clone(),
                index: 0,
            },
        ),
        Transform::from_xyz(-(WINDOW_RESOLUTION.0 as f32) / 2. + 180., -185., 1.)
            .with_scale(Vec3::splat(SONIC_SPRITE_SCALE)),
        run_animation,
        AnimationTimer(Timer::from_seconds(0.04, TimerMode::Repeating)),
    ));
}
