use bevy::{
    ecs::{
        entity::{ContainsEntity, Entity},
        query::With,
        system::{Commands, Res, ResMut, Single},
    },
    math::{Vec2, Vec3},
    sprite::{Sprite, Text2d},
    text::{Justify, TextColor, TextFont, TextLayout},
    time::Time,
    transform::components::Transform,
};

use crate::{
    core::{
        BACKGROUND_COLOR, CANVAS_COLOR, DEFAULT_FONT_SIZE, DEFAULT_TEXT_COLOR, GAME_OVER_FONT_SIZE,
        GAME_OVER_TEXT_COLOR, GameFonts, GameStartingTimer, Grid, GridPosition, WINDOW_RESOLUTION,
    },
    plugins::{
        shared::get_score_text_right_offset,
        window::{GameOverText, GameStartingText},
    },
};

pub fn draw_background(mut commands: Commands) {
    let window_size = Vec2::new(WINDOW_RESOLUTION.0 as f32, WINDOW_RESOLUTION.1 as f32);

    commands.spawn((
        Sprite::from_color(BACKGROUND_COLOR, window_size),
        Transform::from_xyz(0., 0., -1.),
    ));
}

pub fn draw_canvas(mut commands: Commands, grid: Res<Grid>) {
    let canvas_size = Vec2::new(
        (grid.size.x * grid.pixels) as f32,
        (grid.size.y * grid.pixels) as f32,
    );

    commands.spawn((
        Sprite::from_color(CANVAS_COLOR, canvas_size),
        Transform::from_xyz(0., 0., -1.),
    ));
}

pub fn draw_instructions(mut commands: Commands, fonts: Res<GameFonts>, grid: Res<Grid>) {
    let offset =
        grid.to_pixels(GridPosition { column: 0, row: 0 }, 1.) + Vec3::new(-200., 300., 0.);

    let text_intructions = "INSTRUCTIONS\n\n\n\n\n\n\n\n
        Left/Right/Top/Bottom\n\nArrow Keys\n\n\n
        Press SPACE to Pause/Unpause\n\n\n
        Press ENTER to Restart";

    let text_font = TextFont {
        font: fonts.bebas_neue_regular.clone(),
        font_size: DEFAULT_FONT_SIZE,
        font_smoothing: bevy::text::FontSmoothing::None,
        ..Default::default()
    };

    let instructions = (
        Text2d::new(text_intructions),
        text_font,
        TextColor(DEFAULT_TEXT_COLOR),
        TextLayout::new_with_justify(Justify::Center),
        Transform::from_translation(offset),
    );

    commands.spawn(instructions);
}

pub fn show_game_starting_text(
    mut commands: Commands,
    mut timer: ResMut<GameStartingTimer>,
    fonts: Res<GameFonts>,
    grid: Res<Grid>,
) {
    let y_offset =
        grid.to_pixels(
            GridPosition {
                column: grid.size.x,
                row: grid.size.y,
            },
            0.,
        )
        .y + 10.;
    let offset = get_score_text_right_offset(&grid, y_offset, 0.);

    let content = "";

    let text_font = TextFont {
        font: fonts.bebas_neue_regular.clone(),
        font_size: DEFAULT_FONT_SIZE,
        font_smoothing: bevy::text::FontSmoothing::None,
        ..Default::default()
    };

    let text = (
        Text2d::new(content),
        text_font,
        TextColor(DEFAULT_TEXT_COLOR),
        TextLayout::new_with_justify(Justify::Center),
        Transform::from_translation(offset),
        GameStartingText,
    );

    commands.spawn(text);
    timer.0.reset();
}

pub fn update_game_starting_text(
    mut commands: Commands,
    time: Res<Time>,
    mut timer: ResMut<GameStartingTimer>,
    text_query: Single<(Entity, &mut Text2d), With<GameStartingText>>,
) {
    let (entity, mut text) = text_query.into_inner();
    timer.0.tick(time.delta());

    if timer.0.is_finished() {
        commands.entity(entity).despawn();
        return;
    }

    let remaining_seconds = timer.0.remaining_secs().ceil();
    text.0 = format!("Game starts in {} seconds ...", remaining_seconds);
}

pub fn show_game_over_text(mut commands: Commands, fonts: Res<GameFonts>) {
    let content = "GAME OVER\n\nPRESS ENTER TO RESTART";

    let text_font = TextFont {
        font: fonts.bebas_neue_regular.clone(),
        font_size: GAME_OVER_FONT_SIZE,
        font_smoothing: bevy::text::FontSmoothing::None,
        ..Default::default()
    };

    let text = (
        Text2d::new(content),
        text_font,
        TextColor(GAME_OVER_TEXT_COLOR),
        TextLayout::new_with_justify(Justify::Center),
        Transform::from_xyz(0.0, 0.0, 1.0),
        GameOverText,
    );

    commands.spawn(text);
}

pub fn hide_game_over_text(mut commands: Commands, text_query: Single<Entity, With<GameOverText>>) {
    commands.entity(text_query.entity()).despawn();
}
