use bevy::{
    color::Color,
    ecs::{
        children,
        observer::On,
        query::With,
        system::{Commands, Res, ResMut, Single},
    },
    math::{Vec2, Vec3},
    sprite::Sprite,
    text::{FontSize, Justify, TextColor, TextFont, TextLayout},
    transform::components::Transform,
    ui::{JustifyContent, Node, PositionType, percent, px, widget::Text},
};

use crate::plugins::{
    BRICK_SCORE, BrickDestroyed, GameInfo, GameTexture, HEART_SCALE, HEART_TEXTURE_SIZE,
    HEART_TOP_OFFSET, Heart, HeartUpgradeDestroyed, SCORE_TEXT_FONT_SIZE, ScoreTextUi,
    WINDOW_RESOLUTION, WINDOW_RESOLUTION_HALF, calculate_heart_horizontal_position,
};

const BACKGROUND_SPRITE_SIZE: Vec2 = Vec2::new(1204., 512.);

pub fn spawn_background(mut commands: Commands, game_texture: Res<GameTexture>) {
    commands.spawn((
        Sprite {
            image: game_texture.background.clone(),
            ..Default::default()
        },
        Transform::from_xyz(0., 0., 0.).with_scale(Vec3::new(
            WINDOW_RESOLUTION.0 as f32 / BACKGROUND_SPRITE_SIZE.x,
            WINDOW_RESOLUTION.1 as f32 / BACKGROUND_SPRITE_SIZE.y,
            1.,
        )),
    ));
}

pub fn spawn_hearts(
    mut commands: Commands,
    game_texture: Res<GameTexture>,
    game_info: Res<GameInfo>,
) {
    for index in 0..game_info.lives {
        let position = Vec2::new(
            calculate_heart_horizontal_position(index),
            WINDOW_RESOLUTION_HALF.y - HEART_TEXTURE_SIZE.y / 2. - HEART_TOP_OFFSET,
        );

        commands.spawn((
            Sprite {
                image: game_texture.heart.clone(),
                ..Default::default()
            },
            Transform::from_translation(position.extend(1.)).with_scale(Vec3::splat(HEART_SCALE)),
            Heart { index },
        ));
    }
}

pub fn spawn_score_text(mut commands: Commands, game_info: Res<GameInfo>) {
    // Create a container that will center everything
    let container = Node {
        width: percent(100.),
        height: percent(100.),
        justify_content: JustifyContent::Center,
        ..Default::default()
    };

    // Then add a container for the text
    let text_container = Node {
        width: px(400.),
        height: px(50.),
        ..Default::default()
    };

    let score = (
        ScoreTextUi,
        Text::new(format!("SCORE: {}", game_info.score)),
        TextFont {
            font_size: FontSize::Px(SCORE_TEXT_FONT_SIZE),
            ..Default::default()
        },
        TextColor(Color::WHITE),
        TextLayout::justify(Justify::Center),
        Node {
            position_type: PositionType::Absolute,
            top: px(10.),
            left: px(-(WINDOW_RESOLUTION.0 as f32) / 2. + 220.),
            ..Default::default()
        },
    );

    commands.spawn((container, children![(text_container, children![score])]));
}

pub fn spawn_new_heart(
    _: On<HeartUpgradeDestroyed>,
    mut commands: Commands,
    game_texture: Res<GameTexture>,
    game_info: Res<GameInfo>,
) {
    let position = Vec2::new(
        calculate_heart_horizontal_position(game_info.lives - 1),
        WINDOW_RESOLUTION_HALF.y - HEART_TEXTURE_SIZE.y / 2. - HEART_TOP_OFFSET,
    );

    commands.spawn((
        Sprite {
            image: game_texture.heart.clone(),
            ..Default::default()
        },
        Transform::from_translation(position.extend(1.)).with_scale(Vec3::splat(HEART_SCALE)),
        Heart {
            index: game_info.lives,
        },
    ));
}

pub fn update_score(
    _: On<BrickDestroyed>,
    mut game_info: ResMut<GameInfo>,
    mut score_text_ui: Single<&mut Text, With<ScoreTextUi>>,
) {
    game_info.score += BRICK_SCORE;
    score_text_ui.0 = format!("SCORE: {}", game_info.score);
}
