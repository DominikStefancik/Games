use bevy::{
    color::Color,
    text::{Justify, TextColor, TextFont, TextLayout},
    ui::{Node, PositionType, px, widget::Text},
};

use crate::{
    plugins::default::WINDOW_RESOLUTION,
    resources::{GameFonts, GameSettings},
};

const GAME_OVER_FONT_SIZE: f32 = 72.;
const SCORE_FONT_SIZE: f32 = 46.;
const RANK_TEXT_FONT_SIZE: f32 = 36.;
const RANK_LETTER_FONT_SIZE: f32 = 72.;
const SUBTEXT_FONT_SIZE: f32 = 30.;

type TextNode = (Text, TextFont, TextColor, TextLayout, Node);

pub fn create_game_over_text(game_fonts: &GameFonts) -> TextNode {
    (
        Text::new("GAME OVER"),
        TextFont {
            font: game_fonts.mania.clone(),
            font_size: GAME_OVER_FONT_SIZE,
            ..Default::default()
        },
        TextColor(Color::WHITE),
        TextLayout::new_with_justify(Justify::Center),
        Node {
            position_type: PositionType::Absolute,
            top: px(150.),
            left: px((WINDOW_RESOLUTION.0 as f32) / 2. - 150.),
            ..Default::default()
        },
    )
}

pub fn create_best_score_text(game_fonts: &GameFonts, game_settings: &GameSettings) -> TextNode {
    (
        Text::new(format!("BEST SCORE: {}", game_settings.best_score)),
        TextFont {
            font: game_fonts.mania.clone(),
            font_size: SCORE_FONT_SIZE,
            ..Default::default()
        },
        TextColor(Color::WHITE),
        TextLayout::new_with_justify(Justify::Center),
        Node {
            position_type: PositionType::Absolute,
            top: px(300.),
            left: px(240.),
            ..Default::default()
        },
    )
}

pub fn create_current_score_text(game_fonts: &GameFonts, game_settings: &GameSettings) -> TextNode {
    (
        Text::new(format!("CURRENT SCORE: {}", game_settings.score)),
        TextFont {
            font: game_fonts.mania.clone(),
            font_size: SCORE_FONT_SIZE,
            ..Default::default()
        },
        TextColor(Color::WHITE),
        TextLayout::new_with_justify(Justify::Center),
        Node {
            position_type: PositionType::Absolute,
            top: px(300.),
            left: px((WINDOW_RESOLUTION.0 as f32) / 2. + 150.),
            ..Default::default()
        },
    )
}

pub fn create_best_rank_text(game_fonts: &GameFonts) -> TextNode {
    (
        Text::new("BEST RANK"),
        TextFont {
            font: game_fonts.mania.clone(),
            font_size: RANK_TEXT_FONT_SIZE,
            ..Default::default()
        },
        TextColor(Color::WHITE),
        TextLayout::new_with_justify(Justify::Center),
        Node {
            position_type: PositionType::Absolute,
            top: px(390.),
            left: px(320.),
            ..Default::default()
        },
    )
}

pub fn create_current_rank_text(game_fonts: &GameFonts) -> TextNode {
    (
        Text::new("CURRENT RANK"),
        TextFont {
            font: game_fonts.mania.clone(),
            font_size: RANK_TEXT_FONT_SIZE,
            ..Default::default()
        },
        TextColor(Color::WHITE),
        TextLayout::new_with_justify(Justify::Center),
        Node {
            position_type: PositionType::Absolute,
            top: px(390.),
            left: px((WINDOW_RESOLUTION.0 as f32) / 2. + 240.),
            ..Default::default()
        },
    )
}

pub fn create_best_rank_letter(game_fonts: &GameFonts, game_settings: &GameSettings) -> TextNode {
    (
        Text::new(game_settings.best_rank),
        TextFont {
            font: game_fonts.mania.clone(),
            font_size: RANK_LETTER_FONT_SIZE,
            ..Default::default()
        },
        TextColor(Color::WHITE),
        TextLayout::new_with_justify(Justify::Center),
        Node {
            position_type: PositionType::Absolute,
            top: px(500.),
            left: px(380.),
            ..Default::default()
        },
    )
}

pub fn create_current_rank_letter(
    game_fonts: &GameFonts,
    game_settings: &GameSettings,
) -> TextNode {
    (
        Text::new(game_settings.rank),
        TextFont {
            font: game_fonts.mania.clone(),
            font_size: RANK_LETTER_FONT_SIZE,
            ..Default::default()
        },
        TextColor(Color::WHITE),
        TextLayout::new_with_justify(Justify::Center),
        Node {
            position_type: PositionType::Absolute,
            top: px(500.),
            left: px((WINDOW_RESOLUTION.0 as f32) / 2. + 330.),
            ..Default::default()
        },
    )
}

pub fn create_play_instructions_text(game_fonts: &GameFonts) -> TextNode {
    (
        Text::new("Press Space/Click/Touch to Play"),
        TextFont {
            font: game_fonts.mania.clone(),
            font_size: SUBTEXT_FONT_SIZE,
            ..Default::default()
        },
        TextColor(Color::WHITE),
        TextLayout::new_with_justify(Justify::Center),
        Node {
            position_type: PositionType::Absolute,
            top: px((WINDOW_RESOLUTION.1 as f32) - 150.),
            left: px((WINDOW_RESOLUTION.0 as f32) / 2. - 220.),
            ..Default::default()
        },
    )
}
