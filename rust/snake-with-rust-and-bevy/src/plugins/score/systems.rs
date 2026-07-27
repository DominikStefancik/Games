use bevy::{
    color::{Alpha, Color},
    ecs::{
        entity::Entity,
        observer::On,
        query::With,
        system::{Commands, Query, Res, ResMut, Single},
    },
    sprite::Text2d,
    text::{FontSmoothing, Justify, TextColor, TextFont, TextLayout},
    time::{Time, Timer, TimerMode},
    transform::components::Transform,
};

use crate::{
    core::{
        BEST_SCORE_COLOR, DEFAULT_FONT_SIZE, DEFAULT_TEXT_COLOR, GameFonts, Grid, SCORE_FONT_SIZE,
        SCORE_TEXT_COLOR, SCORE_TEXT_Y_OFFSET,
    },
    plugins::{
        score::{
            BestScoreLabelUi, BestScoreTextUi, Score, ScoreLabelUi, ScorePop, ScoreTextUi,
            spawn_score_text,
        },
        shared::{FoodConsumed, get_score_text_right_offset},
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
        SCORE_TEXT_Y_OFFSET,
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

// We create a ScorePop entity every time a food is consumed
pub fn spawn_score_pop(
    _: On<FoodConsumed>,
    mut commands: Commands,
    fonts: Res<GameFonts>,
    grid: Res<Grid>,
    score: Res<Score>,
) {
    // We spawn a ScorePop entity, a white version of the score text that floats upward and fades.
    commands.spawn((
        Text2d::new(score.current.to_string()),
        TextFont {
            font: fonts.bebas_neue_regular.clone(),
            font_size: SCORE_FONT_SIZE,
            font_smoothing: FontSmoothing::None,
            ..Default::default()
        },
        TextLayout::new_with_justify(Justify::Center),
        TextColor(Color::WHITE),
        Transform::from_translation(get_score_text_right_offset(&grid, SCORE_TEXT_Y_OFFSET, 2.)),
        ScorePop(Timer::from_seconds(0.6, TimerMode::Once)),
    ));
}

pub fn increase_current_score(
    _: On<FoodConsumed>,
    mut score: ResMut<Score>,
    mut text_query: Single<&mut Text2d, With<ScoreTextUi>>,
) {
    score.current += 1;
    text_query.0 = score.current.to_string();
}

// This system is called on every Update cycle,
// so we can gradually update the ScorePop text's position and color alpha.
// This way we achieve popping fading effect, which will disappear after the time is finished.
pub fn update_score_pop(
    mut commands: Commands,
    time: Res<Time>,
    score_pop_query: Query<(Entity, &mut ScorePop, &mut Transform, &mut TextColor)>,
) {
    for (entity, mut score_pop, mut transform, mut text_color) in score_pop_query {
        score_pop.0.tick(time.delta());

        if score_pop.0.is_finished() {
            commands.entity(entity).despawn();
            return;
        }

        /*
         * The "fraction_remaining()" goes from 1.0 at the start of the timer down to 0.0 at the end.
         * We use it for both color alpha (fades out) and to drive the upward float.
         */
        let time_fraction_remaining = score_pop.0.fraction_remaining();
        /*
         * When time_fraction_remaining = 1.0 (just spawned), y = SCORE_TEXT_Y_OFFSET + 0.0 * 80.0 = SCORE_TEXT_Y_OFFSET.
         * When time_fraction_remaining = 0.0 (about to despawn), y = SCORE_TEXT_Y_OFFSET + 1.0 * 80.0 = SCORE_TEXT_Y_OFFSET + 80.0.
         * So the text floats 80 pixels upward while fading.
         */
        transform.translation.y = SCORE_TEXT_Y_OFFSET + (1. - time_fraction_remaining) * 80.;
        text_color.0.set_alpha(time_fraction_remaining);
    }
}

pub fn update_best_score(
    mut score: ResMut<Score>,
    mut text_query: Single<&mut Text2d, With<BestScoreTextUi>>,
) {
    if score.current > score.best {
        score.best = score.current;
        text_query.0 = score.current.to_string();
    }
}
