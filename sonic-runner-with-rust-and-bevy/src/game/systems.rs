use bevy::{
    asset::Handle,
    audio::{AudioPlayer, AudioSink, AudioSinkPlayback, AudioSource, PlaybackSettings, Volume},
    color::Color,
    ecs::{
        change_detection::DetectChanges,
        children,
        entity::{ContainsEntity, Entity},
        observer::On,
        query::With,
        spawn::SpawnRelated,
        system::{Commands, Res, ResMut, Single},
    },
    input::{ButtonInput, keyboard::KeyCode},
    state::state::{NextState, State},
    text::{Justify, TextColor, TextFont, TextLayout},
    ui::{JustifyContent, Node, PositionType, percent, px, widget::Text},
};

use crate::{
    game::{GameState, components::GameScoreTextUi, events::GameScoreUpdated},
    plugins::default::WINDOW_RESOLUTION,
    resources::{GameFonts, GameSettings, GameSounds},
    scene::components::BackgroundMusic,
};

const GAME_SCORE_FONT_SIZE: f32 = 52.;

pub fn reset_game_settings(mut game_settings: ResMut<GameSettings>) {
    game_settings.reset();
}

pub fn spawn_score_text(
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
        width: px(400.),
        height: px(50.),
        ..Default::default()
    };

    let score = (
        GameScoreTextUi,
        Text::new(format!("SCORE: {}", game_settings.score)),
        TextFont {
            font: game_fonts.mania.clone(),
            font_size: GAME_SCORE_FONT_SIZE,
            ..Default::default()
        },
        TextColor(Color::WHITE),
        TextLayout::new_with_justify(Justify::Center),
        Node {
            position_type: PositionType::Absolute,
            top: px(10.),
            left: px(-(WINDOW_RESOLUTION.0 as f32) / 2. + 220.),
            ..Default::default()
        },
    );

    commands.spawn((container, children![(text_container, children![score])]));
}

pub fn despawn_score_text(
    mut commands: Commands,
    text_container: Single<Entity, With<GameScoreTextUi>>,
) {
    commands.entity(text_container.entity()).despawn();
}

pub fn toggle_pausing_game(
    keyboard_input: Res<ButtonInput<KeyCode>>,
    game_state: Res<State<GameState>>,
    mut next_state: ResMut<NextState<GameState>>,
) {
    if keyboard_input.just_pressed(KeyCode::KeyP) {
        match game_state.get() {
            GameState::Running => {
                next_state.set(GameState::Paused);
            }
            GameState::Paused => {
                next_state.set(GameState::Running);
            }
        }
    }
}

pub fn spawn_background_music(mut commands: Commands, game_sounds: Res<GameSounds>) {
    commands.spawn((
        AudioPlayer::new(game_sounds.background.clone()),
        PlaybackSettings::LOOP.with_volume(Volume::Linear(0.25)),
        BackgroundMusic,
    ));
}

pub fn pause_background_music(
    keyboard_input: Res<ButtonInput<KeyCode>>,
    music_query: Single<&AudioSink, With<BackgroundMusic>>,
) {
    if keyboard_input.just_pressed(KeyCode::KeyP) {
        let sink = music_query.into_inner();
        sink.toggle_playback();
    }
}

pub fn spawn_sound(commands: &mut Commands, sound: &Handle<AudioSource>) {
    commands.spawn((
        AudioPlayer::new(sound.clone()),
        PlaybackSettings::DESPAWN.with_volume(Volume::Linear(0.5)),
    ));
}

pub fn update_game_score_text(
    _: On<GameScoreUpdated>,
    game_settings: Res<GameSettings>,
    mut score_text_ui: Single<&mut Text, With<GameScoreTextUi>>,
) {
    if game_settings.is_changed() {
        score_text_ui.0 = format!("SCORE: {}", game_settings.score);
    }
}
