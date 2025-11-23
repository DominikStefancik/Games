use bevy::{
    asset::AssetServer,
    camera::Camera2d,
    color::Color,
    ecs::{
        children,
        query::With,
        spawn::SpawnRelated,
        system::{Commands, Query, Res},
    },
    math::Vec3,
    sprite::Sprite,
    text::{Justify, TextColor, TextFont, TextLayout},
    time::{Time, Timer, TimerMode},
    transform::components::Transform,
    ui::{JustifyContent, Node, PositionType, percent, px, widget::Text},
};

use crate::plugins::{
    default::WINDOW_RESOLUTION,
    scene::components::{Background, Platform, Scrollable, ScrollingTimer},
};

const BACKGROUND_SPRITE_WIDTH: f32 = 1920.;
const BACKGROUND_SPRITE_SCALE: f32 = 1.7;
const PLATFORM_SPRITE_WIDTH: f32 = 1280.;
const PLATFORM_SPRITE_SCALE: f32 = 3.2;
const GAME_NAME_FONT_SIZE: f32 = 72.;
const INSTRUCTIONS_FONT_SIZE: f32 = 30.;

pub fn spawn_camera(mut commands: Commands) {
    commands.spawn(Camera2d);
}

pub fn spawn_background(mut commands: Commands, asset_server: Res<AssetServer>) {
    let texture = asset_server.load("graphics/chemical-background.png");
    // Alpha channel of the color controls transparency
    let color = Color::srgba(1.0, 1.0, 1.0, 0.9);
    let pixels_to_scroll = 3.;
    let timer = Timer::from_seconds(0.005, TimerMode::Repeating);
    let vertical_position_value = -435.;

    commands.spawn((
        Sprite {
            image: texture.clone(),
            color,
            ..Default::default()
        },
        Transform::from_xyz(0., vertical_position_value, 0.)
            .with_scale(Vec3::splat(BACKGROUND_SPRITE_SCALE)),
        Scrollable::new(pixels_to_scroll),
        ScrollingTimer(timer.clone()),
        Background,
    ));

    commands.spawn((
        Sprite {
            image: texture.clone(),
            color,
            ..Default::default()
        },
        // we want to position the "second" background image right after the first one
        // but since we scaled the image, we have to add BACKGROUND_SPRITE_WIDTH * BACKGROUND_SPRITE_SCALE
        Transform::from_xyz(
            BACKGROUND_SPRITE_WIDTH * BACKGROUND_SPRITE_SCALE,
            vertical_position_value,
            0.,
        )
        .with_scale(Vec3::splat(BACKGROUND_SPRITE_SCALE)),
        Scrollable::new(pixels_to_scroll),
        ScrollingTimer(timer),
        Background,
    ));
}

pub fn spawn_platform(mut commands: Commands, asset_server: Res<AssetServer>) {
    let texture = asset_server.load("graphics/platforms.png");
    let pixels_to_scroll = 15.;
    let timer = Timer::from_seconds(0.0001, TimerMode::Repeating);
    let vertical_position_value = -200.;

    commands.spawn((
        Sprite::from_image(texture.clone()),
        Transform::from_xyz(0., vertical_position_value, 1.)
            .with_scale(Vec3::splat(PLATFORM_SPRITE_SCALE)),
        Scrollable::new(pixels_to_scroll),
        ScrollingTimer(timer.clone()),
        Platform,
    ));

    commands.spawn((
        Sprite::from_image(texture.clone()),
        // we want to position the "second" platforms image right after the first one
        // but since we scaled the image, we have to add PLATFORMS_SPRITE_WIDTH * PLATFORM_SPRITE_SCALE
        Transform::from_xyz(
            PLATFORM_SPRITE_WIDTH * PLATFORM_SPRITE_SCALE,
            vertical_position_value,
            1.,
        )
        .with_scale(Vec3::splat(PLATFORM_SPRITE_SCALE)),
        Scrollable::new(pixels_to_scroll),
        ScrollingTimer(timer),
        Platform,
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

pub fn scroll_background(
    time: Res<Time>,
    mut query: Query<(&Scrollable, &mut ScrollingTimer, &mut Transform), With<Background>>,
) {
    let half_window_width = (WINDOW_RESOLUTION.0 / 2) as f32;
    let half_background_width = (BACKGROUND_SPRITE_WIDTH * BACKGROUND_SPRITE_SCALE) / 2.;

    for (scrollable, mut timer, mut transform) in &mut query {
        timer.tick(time.delta());

        if timer.just_finished() {
            transform.translation.x -= scrollable.pixels_to_scroll;

            // what we do here is to replace the order of the background components
            // the "first" component will become the "second" and the "second" will become the "first"
            // this way we will achieve the effect of an infinite scrolling background
            if transform.translation.x < -half_background_width - half_window_width {
                transform.translation.x = BACKGROUND_SPRITE_WIDTH * BACKGROUND_SPRITE_SCALE
                    + half_window_width
                    + half_window_width / BACKGROUND_SPRITE_SCALE
                    - 180.;
            }
        }
    }
}

pub fn scroll_platform(
    time: Res<Time>,
    mut query: Query<(&Scrollable, &mut ScrollingTimer, &mut Transform), With<Platform>>,
) {
    let half_window_width = (WINDOW_RESOLUTION.0 / 2) as f32;
    let half_platform_width = (PLATFORM_SPRITE_WIDTH * PLATFORM_SPRITE_SCALE) / 2.;

    for (scrollable, mut timer, mut transform) in &mut query {
        timer.tick(time.delta());

        if timer.just_finished() {
            transform.translation.x -= scrollable.pixels_to_scroll;

            // what we do here is to replace the order of the background components
            // the "first" component will become the "second" and the "second" will become the "first"
            // this way we will achieve the effect of an infinite scrolling platform
            if transform.translation.x < -half_platform_width - half_window_width {
                transform.translation.x = PLATFORM_SPRITE_WIDTH * PLATFORM_SPRITE_SCALE
                    + half_window_width
                    + half_window_width / PLATFORM_SPRITE_SCALE
                    - 180.;
            }
        }
    }
}
