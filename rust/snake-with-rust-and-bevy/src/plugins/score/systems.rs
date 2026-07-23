use bevy::{
    ecs::{
        observer::On,
        query::With,
        system::{Commands, Res, ResMut, Single},
    },
    sprite::Text2d,
};

use crate::{
    core::{
        BEST_SCORE_COLOR, DEFAULT_FONT_SIZE, DEFAULT_TEXT_COLOR, GameFonts, Grid, SCORE_FONT_SIZE,
        SCORE_TEXT_COLOR,
    },
    plugins::{
        score::{
            BestScoreLabelUi, BestScoreTextUi, Score, ScoreLabelUi, ScoreTextUi, spawn_score_text,
        },
        shared::FoodConsumed,
    },
};

pub fn spawn_score(
    mut commands: Commands,
    fonts: Res<GameFonts>,
    grid: Res<Grid>,
    score: Res<Score>,
) {
    spawn_score_text(
        &mut commands,
        fonts.bebas_neue_regular.clone(),
        DEFAULT_FONT_SIZE,
        DEFAULT_TEXT_COLOR,
        &grid,
        215.,
        "Score",
        ScoreLabelUi,
    );

    spawn_score_text(
        &mut commands,
        fonts.bebas_neue_regular.clone(),
        SCORE_FONT_SIZE,
        SCORE_TEXT_COLOR,
        &grid,
        100.,
        &score.current.to_string(),
        ScoreTextUi,
    );

    spawn_score_text(
        &mut commands,
        fonts.bebas_neue_regular.clone(),
        DEFAULT_FONT_SIZE,
        DEFAULT_TEXT_COLOR,
        &grid,
        -85.,
        "Best Score",
        BestScoreLabelUi,
    );

    spawn_score_text(
        &mut commands,
        fonts.bebas_neue_regular.clone(),
        SCORE_FONT_SIZE,
        BEST_SCORE_COLOR,
        &grid,
        -200.,
        &score.best.to_string(),
        BestScoreTextUi,
    );
}

pub fn update_score(
    _: On<FoodConsumed>,
    mut score: ResMut<Score>,
    mut text_query: Single<&mut Text2d, With<ScoreTextUi>>,
) {
    score.current += 1;
    text_query.0 = score.current.to_string();
}
