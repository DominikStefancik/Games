use bevy::{
    asset::{AssetServer, Handle},
    audio::{AudioPlayer, AudioSink, AudioSinkPlayback, AudioSource, PlaybackSettings, Volume},
    ecs::{
        query::With,
        system::{Commands, Res, ResMut, Single},
    },
    input::{ButtonInput, keyboard::KeyCode},
    state::state::{NextState, State},
};

use crate::{game::GameState, scenes::components::BackgroundMusic};

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

pub fn spawn_background_music(mut commands: Commands, asset_server: Res<AssetServer>) {
    commands.spawn((
        AudioPlayer::new(asset_server.load("sounds/City.mp3")),
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

pub fn spawn_sound(commands: &mut Commands, sound: Handle<AudioSource>) {
    commands.spawn((
        AudioPlayer::new(sound),
        PlaybackSettings::DESPAWN.with_volume(Volume::Linear(0.5)),
    ));
}
