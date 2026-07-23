use bevy::{
    ecs::system::{Commands, Res},
    math::{Vec2, Vec3},
    sprite::{Sprite, Text2d},
    text::{Justify, TextColor, TextFont, TextLayout},
    transform::components::Transform,
};

use crate::core::{
    BACKGROUND_COLOR, CANVAS_COLOR, DEFAULT_FONT_SIZE, DEFAULT_TEXT_COLOR, GameFonts, Grid,
    GridPosition, WINDOW_RESOLUTION,
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
        Press R to Reset";

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
