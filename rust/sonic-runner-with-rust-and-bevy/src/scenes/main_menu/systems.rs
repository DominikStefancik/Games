use bevy::{
    color::Color,
    ecs::{
        children,
        entity::{ContainsEntity, Entity},
        query::With,
        system::{Commands, Res, Single},
    },
    text::{Justify, TextColor, TextFont, TextLayout},
    ui::{JustifyContent, Node, PositionType, percent, px, widget::Text},
};

use crate::{resources::GameFonts, scenes::main_menu::components::MainMenuTextUi};

const GAME_NAME_FONT_SIZE: f32 = 72.;
const SUBTEXT_FONT_SIZE: f32 = 30.;

pub fn spawn_main_text(mut commands: Commands, game_fonts: Res<GameFonts>) {
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
            font: game_fonts.mania.clone(),
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

    let play_instructions = (
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
            top: px(250.),
            left: px(20.),
            ..Default::default()
        },
    );

    let pause_instructions = (
        Text::new("Press P to Pause or Unpause"),
        TextFont {
            font: game_fonts.mania.clone(),
            font_size: SUBTEXT_FONT_SIZE,
            ..Default::default()
        },
        TextColor(Color::WHITE),
        TextLayout::new_with_justify(Justify::Center),
        Node {
            position_type: PositionType::Absolute,
            top: px(300.),
            left: px(40.),
            ..Default::default()
        },
    );

    commands.spawn((
        MainMenuTextUi,
        container,
        children![(
            text_container,
            children![game_name, play_instructions, pause_instructions]
        )],
    ));
}

pub fn despawn_main_text(
    mut commands: Commands,
    text_container: Single<Entity, With<MainMenuTextUi>>,
) {
    commands.entity(text_container.entity()).despawn();
}
