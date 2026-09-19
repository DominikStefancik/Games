use bevy::{
    color::Color,
    ecs::{
        children,
        entity::{ContainsEntity, Entity},
        observer::On,
        query::With,
        system::{Commands, Res, ResMut, Single},
    },
    math::{Vec2, Vec3},
    sprite::Sprite,
    state::state::{NextState, State},
    text::{FontSize, Justify, TextColor, TextFont, TextLayout},
    transform::components::Transform,
    ui::{JustifyContent, Node, PositionType, percent, px, widget::Text},
};

use crate::plugins::{
    BRICK_SCORE, BallFallenDown, BrickCollided, GAME_FINISHED_FONT_SIZE, GameEntities,
    GameFinishedTextUi, GameInfo, GameRestarted, GameState, GameTexture, HeartUpgradeDestroyed,
    SCORE_TEXT_FONT_SIZE, SUBTEXT_FONT_SIZE, ScoreTextUi, WINDOW_RESOLUTION,
    WINDOW_RESOLUTION_HALF, spawn_all_hearts, spawn_single_heart,
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
    spawn_all_hearts(&mut commands, &game_texture, game_info.lives);
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
    mut game_info: ResMut<GameInfo>,
) {
    if game_info.lives < game_info.max_lives {
        spawn_single_heart(&mut commands, &game_texture, game_info.lives);

        game_info.lives += 1;
    }
}

pub fn update_score(
    _: On<BrickCollided>,
    mut game_info: ResMut<GameInfo>,
    mut score_text_ui: Single<&mut Text, With<ScoreTextUi>>,
) {
    game_info.score += BRICK_SCORE;
    score_text_ui.0 = format!("SCORE: {}", game_info.score);
}

pub fn restart_game(
    _: On<GameRestarted>,
    mut next_state: ResMut<NextState<GameState>>,
    game_texture: Res<GameTexture>,
    mut game_info: ResMut<GameInfo>,
    mut game_entities: GameEntities,
    mut score_text_ui: Single<&mut Text, With<ScoreTextUi>>,
) {
    game_entities.reset_moving_elements();
    game_entities.despawn_bricks();
    // In the case the game is restarted after a player won, there are hearts left which we have to despawn
    game_entities.despawn_all_hearts();

    game_info.reset();
    score_text_ui.0 = format!("SCORE: {}", game_info.score);
    spawn_all_hearts(&mut game_entities.commands, &game_texture, game_info.lives);

    next_state.set(GameState::NewLevelStarting);
}

pub fn restart_running_state(
    _: On<BallFallenDown>,
    mut next_state: ResMut<NextState<GameState>>,
    mut game_info: ResMut<GameInfo>,
    mut game_entities: GameEntities,
) {
    /*
     * StateTransition runs once per frame, after PreUpdate, i.e. before RunFixedMainLoop.
     * FixedUpdate therefore never sees a state change mid-frame. With the default 64 Hz timestep
     * (Duration::from_micros(15625)) and a 60 Hz monitor, the accumulator produces two fixed ticks in roughly every
     * fourth frame.
     *
     * If we trace the last life:
     *      Tick 1: check_ball_out_of_bounds → BallFallenDown → observer runs at that tick’s command flush →
     *              lives: 1 → 0 → GameOver queued. The ball is not reset — that only happens in the else branch,
     *              so it’s still below the screen and still has a downward direction.
     *      Tick 2, same frame: in_state(Running) is still true. move_ball_when_game_runs pushes it further down,
     *              check_ball_out_of_bounds fires again → lives: 0 - 1.
     * Debug build: panic, attempt to subtract with overflow.
     * Release build: wraps to 65535, the == 0 check fails, so the else branch runs and calls
     * next_state.set(GameState::BallReady) — which overwrites the pending GameOver. The player keeps playing with
     * 65,535 invisible lives and game over never triggers again.
     *
     * This isn’t reachable in the Update phase, because in Update the system runs exactly once per frame and
     * the transition always lands first.
     * To fix this for the FixedUpdate phase we need to:
     *      1. Reset the ball’s position in the lives == 0 branch too, so the second tick isn’t out of bounds.
     *      2. Set "game_info.lives = game_info.lives.saturating_sub(1)" as a belt-and-braces guard.
     *
     */
    game_info.lives = game_info.lives.saturating_sub(1);

    game_entities.despawn_heart(game_info.lives);

    if game_info.lives == 0 {
        game_entities.reset_ball();
        next_state.set(GameState::GameOver);
    } else {
        game_entities.reset_moving_elements();
        next_state.set(GameState::BallReady);
    }
}

pub fn is_level_finished(
    mut next_state: ResMut<NextState<GameState>>,
    mut game_info: ResMut<GameInfo>,
    mut game_entities: GameEntities,
) {
    if game_entities.brick_query.is_empty() {
        if game_info.is_last_level() {
            next_state.set(GameState::GameWin);
        } else {
            game_entities.reset_moving_elements();

            game_info.move_to_next_level();
            next_state.set(GameState::NewLevelStarting);
        }
    }
}

pub fn spawn_game_finished_text(mut commands: Commands, app_state: Res<State<GameState>>) {
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

    let mut text = "";
    let mut horizontal_offset = 0.;

    if *app_state == GameState::GameWin {
        text = "YOU WON!";
        horizontal_offset = 150.;
    } else if *app_state == GameState::GameOver {
        text = "GAME OVER";
        horizontal_offset = 190.;
    }

    let game_over = (
        Text::new(text),
        TextFont {
            font_size: FontSize::Px(GAME_FINISHED_FONT_SIZE),
            ..Default::default()
        },
        TextColor(Color::WHITE),
        TextLayout::justify(Justify::Center),
        Node {
            position_type: PositionType::Absolute,
            top: px(180.),
            left: px(WINDOW_RESOLUTION_HALF.x - horizontal_offset),
            ..Default::default()
        },
    );

    let play_instructions = (
        Text::new("Press Space to play again"),
        TextFont {
            font_size: FontSize::Px(SUBTEXT_FONT_SIZE),
            ..Default::default()
        },
        TextColor(Color::WHITE),
        TextLayout::justify(Justify::Center),
        Node {
            position_type: PositionType::Absolute,
            top: px(300.),
            left: px(WINDOW_RESOLUTION_HALF.x - 230.),
            ..Default::default()
        },
    );

    commands.spawn((
        GameFinishedTextUi,
        container,
        children![(text_container, children![game_over, play_instructions])],
    ));
}

pub fn despawn_game_finished_text(
    mut commands: Commands,
    text_container: Single<Entity, With<GameFinishedTextUi>>,
) {
    commands.entity(text_container.entity()).despawn();
}
