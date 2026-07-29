use bevy::{
    asset::Handle,
    color::Color,
    ecs::{component::Component, system::Commands},
    sprite::Text2d,
    text::{Font, FontSize, FontSmoothing, Justify, TextColor, TextFont, TextLayout},
    transform::components::Transform,
};

use crate::plugins::shared::{Grid, get_score_text_right_offset};

#[allow(clippy::too_many_arguments)]
pub fn spawn_score_text(
    commands: &mut Commands,
    font: Handle<Font>,
    font_size: f32,
    text_color: Color,
    grid: &Grid,
    y_offset: f32,
    text: &str,
    ui_marker: impl Component,
) {
    let score_text_offset = get_score_text_right_offset(grid, y_offset, 1.);
    let score_text_style = TextFont {
        font: font.into(),
        font_size: FontSize::Px(font_size),
        font_smoothing: FontSmoothing::None,
        ..Default::default()
    };

    commands.spawn((
        Text2d::new(text),
        score_text_style.clone(),
        TextLayout::justify(Justify::Center),
        TextColor(text_color),
        Transform::from_translation(score_text_offset),
        ui_marker,
    ));
}
