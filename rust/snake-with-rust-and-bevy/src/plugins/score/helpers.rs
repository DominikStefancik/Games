use bevy::{
    asset::Handle,
    color::Color,
    ecs::{component::Component, system::Commands},
    math::Vec3,
    sprite::Text2d,
    text::{Font, FontSmoothing, Justify, TextColor, TextFont, TextLayout},
    transform::components::Transform,
};

use crate::core::{Grid, GridPosition};

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
    let score_label_offset = grid.to_pixels(GridPosition::new(grid.size.x, grid.size.y / 2), 1.)
        + Vec3::new(80., y_offset, 0.);
    let score_label_style = TextFont {
        font,
        font_size,
        font_smoothing: FontSmoothing::None,
        ..Default::default()
    };

    commands.spawn((
        Text2d::new(text),
        score_label_style.clone(),
        TextLayout::new_with_justify(Justify::Center),
        TextColor(text_color),
        Transform::from_translation(score_label_offset),
        ui_marker,
    ));
}
