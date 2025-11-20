use bevy::{
    app::{App, Startup},
    asset::{AssetServer, Assets},
    camera::Camera2d,
    color::Color,
    ecs::{
        children,
        spawn::SpawnRelated,
        system::{Commands, Res, ResMut},
    },
    image::{TextureAtlas, TextureAtlasLayout},
    math::{UVec2, Vec3},
    prelude::Plugin,
    sprite::Sprite,
    text::{Justify, TextColor, TextFont, TextLayout},
    transform::components::Transform,
    ui::{JustifyContent, Node, PositionType, percent, px, widget::Text},
};

use crate::plugins::default::WINDOW_RESOLUTION;

const BACKGROUND_SPRITE_SCALE: f32 = 1.7;
const PLATFORM_SPRITE_SCALE: f32 = 3.2;
const SONIC_SPRITE_SCALE: f32 = 3.;
const GAME_NAME_FONT_SIZE: f32 = 72.;
const INSTRUCTIONS_FONT_SIZE: f32 = 30.;

pub struct ScenePlugin;

impl Plugin for ScenePlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(
            Startup,
            (
                spawn_camera,
                spawn_background,
                spawn_platform,
                spawn_sonic,
                spawn_main_text,
            ),
        );
    }
}

fn spawn_camera(mut commands: Commands) {
    commands.spawn(Camera2d);
}

fn spawn_background(mut commands: Commands, asset_server: Res<AssetServer>) {
    let texture = asset_server.load("graphics/chemical-background.png");

    commands.spawn((
        Sprite {
            image: texture.clone(),
            // Alpha channel of the color controls transparency
            color: Color::srgba(1.0, 1.0, 1.0, 0.8),
            ..Default::default()
        },
        Transform::from_xyz(0., -435., 0.).with_scale(Vec3::splat(BACKGROUND_SPRITE_SCALE)),
    ));
}

fn spawn_platform(mut commands: Commands, asset_server: Res<AssetServer>) {
    let texture = asset_server.load("graphics/platforms.png");

    commands.spawn((
        Sprite::from_image(texture.clone()),
        Transform::from_xyz(0., -200., 1.).with_scale(Vec3::splat(PLATFORM_SPRITE_SCALE)),
    ));
}

fn spawn_sonic(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
    mut texture_atlas_layouts: ResMut<Assets<TextureAtlasLayout>>,
) {
    let texture = asset_server.load("graphics/sonic.png");
    let layout = TextureAtlasLayout::from_grid(UVec2::new(32, 44), 8, 2, None, None);
    let texture_atlas_layout = texture_atlas_layouts.add(layout);

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
    ));
}

pub fn spawn_main_text(mut commands: Commands, asset_server: Res<AssetServer>) {
    let font_handle = asset_server.load("fonts/mania.ttf");

    // Create a container that will center everything
    let container = Node {
        width: percent(100.),
        height: percent(100.),
        justify_content: JustifyContent::Center,
        ..Default::default()
    };

    // Then add a container for the text
    let text_container = Node {
        width: px(480.),
        height: px(500.),
        ..Default::default()
    };

    let game_name = (
        Text::new("SONIC RING RUN"),
        TextFont {
            font: font_handle.clone(),
            font_size: GAME_NAME_FONT_SIZE,
            ..Default::default()
        },
        TextColor(Color::WHITE),
        TextLayout::new_with_justify(Justify::Center),
        Node {
            position_type: PositionType::Absolute,
            top: px(100.),
            left: px(0.),
            ..Default::default()
        },
    );

    let instructions = (
        Text::new("Press Space/Click/Touch to Play"),
        TextFont {
            font: font_handle.clone(),
            font_size: INSTRUCTIONS_FONT_SIZE,
            ..Default::default()
        },
        TextColor(Color::WHITE),
        TextLayout::new_with_justify(Justify::Center),
        Node {
            position_type: PositionType::Absolute,
            top: px(250.),
            left: px(20.),
            ..Default::default()
        },
    );

    commands.spawn((
        container,
        children![(text_container, children![game_name, instructions])],
    ));
}
