use bevy::{
    ecs::{
        children,
        entity::{ContainsEntity, Entity},
        query::With,
        spawn::SpawnRelated,
        system::{Commands, Res, ResMut, Single},
    },
    ui::{JustifyContent, Node, percent, px},
};

use crate::{
    plugins::default::WINDOW_RESOLUTION,
    resources::{GameFonts, GameSettings, RankGrade},
    scenes::game_over::{
        components::GameOverTextUi,
        helpers::{
            create_best_rank_letter, create_best_rank_text, create_best_score_text,
            create_current_rank_letter, create_current_rank_text, create_current_score_text,
            create_game_over_text, create_play_instructions_text,
        },
    },
};

pub fn spawn_game_over_text(
    mut commands: Commands,
    game_fonts: Res<GameFonts>,
    game_settings: Res<GameSettings>,
) {
    // Create a container that will center everything
    let container = Node {
        width: percent(100.),
        height: percent(100.),
        justify_content: JustifyContent::Center,
        ..Default::default()
    };

    // Then add a container for the text
    let text_container = Node {
        width: px(WINDOW_RESOLUTION.0),
        height: px(WINDOW_RESOLUTION.1),
        ..Default::default()
    };

    let game_over = create_game_over_text(&game_fonts);
    let best_score = create_best_score_text(&game_fonts, &game_settings);
    let current_score = create_current_score_text(&game_fonts, &game_settings);
    let best_rank_text = create_best_rank_text(&game_fonts);
    let current_rank_text = create_current_rank_text(&game_fonts);
    let best_rank_letter = create_best_rank_letter(&game_fonts, &game_settings);
    let current_rank_letter = create_current_rank_letter(&game_fonts, &game_settings);
    let play_instructions = create_play_instructions_text(&game_fonts);

    commands.spawn((
        GameOverTextUi,
        container,
        children![(
            text_container,
            children![
                game_over,
                best_score,
                current_score,
                best_rank_text,
                current_rank_text,
                best_rank_letter,
                current_rank_letter,
                play_instructions,
            ]
        )],
    ));
}

pub fn despawn_game_over_text(
    mut commands: Commands,
    text_container: Single<Entity, With<GameOverTextUi>>,
) {
    commands.entity(text_container.entity()).despawn();
}

pub fn update_best_score(mut game_settings: ResMut<GameSettings>) {
    if game_settings.best_score < game_settings.score {
        game_settings.best_score = game_settings.score;
        game_settings.best_rank = RankGrade::from(game_settings.best_score);
    }
}
