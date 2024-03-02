use crate::components::{Ball, Player, ScoreBoard, Side, Sound};
use crate::constants::{ARENA_HEIGHT, ARENA_WIDTH, BALL_RADIUS, BALL_VELOCITY, SCORE_FONT_SIZE};
use bevy::audio::Volume;
use bevy::prelude::{
    AudioBundle, AudioSource, Color, Commands, Handle, Image, PlaybackSettings, SpriteSheetBundle,
    Style, Text, TextBundle, TextStyle, TextureAtlas, TextureAtlasLayout, Transform, Val,
};
use bevy::text::Font;

pub fn spawn_player(
    commands: &mut Commands,
    texture_atlas_layout_handle: Handle<TextureAtlasLayout>,
    sprite_sheet_handle: Handle<Image>,
    cat_sprite_index: usize,
    side: Side,
    x: f32,
    y: f32,
) {
    commands.spawn((
        // the "sprite" field initialization is covered by the `..default()` expression
        SpriteSheetBundle {
            // The TextureAtlas is a single location where we can store all texture atlases in the whole program
            atlas: TextureAtlas {
                layout: texture_atlas_layout_handle,
                index: cat_sprite_index,
            },
            texture: sprite_sheet_handle,
            transform: Transform::from_xyz(x, y, 0.),
            ..Default::default()
        },
        Player { side },
    ));
}

pub fn spawn_ball(
    commands: &mut Commands,
    texture_atlas_layout_handle: Handle<TextureAtlasLayout>,
    sprite_sheet_handle: Handle<Image>,
    ball_sprite_index: usize,
    bounce_sound: Handle<AudioSource>,
    score_sound: Handle<AudioSource>,
) {
    commands.spawn((
        // the "sprite" field initialization is covered by the `..default()` expression
        SpriteSheetBundle {
            // The TextureAtlas is a single location where we can store all texture atlases in the whole program
            atlas: TextureAtlas {
                layout: texture_atlas_layout_handle,
                index: ball_sprite_index,
            },
            texture: sprite_sheet_handle,
            transform: Transform::from_xyz(ARENA_WIDTH / 2., ARENA_HEIGHT / 2., 0.),
            ..Default::default()
        },
        Ball {
            radius: BALL_RADIUS,
            velocity: BALL_VELOCITY,
            bounce_sound,
            score_sound,
        },
    ));
}

pub fn spawn_scoreboard(
    commands: &mut Commands,
    score_font_handle: Handle<Font>,
    side: Side,
    x: f32,
) {
    commands.spawn((
        TextBundle {
            text: Text::from_section(
                "0",
                TextStyle {
                    font: score_font_handle,
                    font_size: SCORE_FONT_SIZE,
                    color: Color::WHITE,
                },
            ),
            style: Style {
                left: Val::Px(x),
                top: Val::Px(25.),
                ..Default::default()
            },
            ..Default::default()
        },
        ScoreBoard { side },
    ));
}

pub fn spawn_sound(commands: &mut Commands, sound: Handle<AudioSource>) {
    commands.spawn((
        AudioBundle {
            source: sound,
            settings: PlaybackSettings::DESPAWN.with_volume(Volume::new(0.5)),
        },
        Sound,
    ));
}
