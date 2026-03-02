mod components;
mod constants;
mod helpers;
mod resources;
mod systems;

use crate::components::{BackgroundMusic, Side};
use crate::constants::{
    ARENA_HEIGHT, ARENA_WIDTH, BACKGROUND_AUDIO_PATH, BALL_SIZE, BALL_TEXTURE_CORNER,
    BOUNCE_AUDIO_PATH, CAT_SIZE, LEFT_CAT_TEXTURE_CORNER, PLAYER_HEIGHT, PLAYER_WIDTH,
    RIGHT_CAT_TEXTURE_CORNER, SCORE_AUDIO_PATH, SCORE_BOARD_LEFT_X, SCORE_BOARD_RIGHT_X,
    SCORE_FONT_PATH, SPRITES_SHEET_PATH, SPRITES_SHEET_SIZE,
};
use crate::helpers::{spawn_ball, spawn_player, spawn_scoreboard};
use crate::resources::Score;
use crate::systems::{
    bounce_ball_system, move_ball_system, move_player_system, pause_background_music_system,
    update_score_system,
};
use bevy::audio::Volume;
use bevy::core_pipeline::core_2d::Camera2d;
use bevy::image::TextureAtlasLayout;
use bevy::prelude::{
    App, AssetServer, Assets, AudioPlayer, ClearColor, Color, Commands, PlaybackSettings,
    PluginGroup, Res, ResMut, Startup, Transform, URect, Update, Window, WindowPlugin,
};
use bevy::DefaultPlugins;

fn main() {
    App::new()
        .add_plugins(DefaultPlugins.set(WindowPlugin {
            primary_window: Some(Window {
                title: "Rust Cat Volleyball".into(),
                resolution: (ARENA_WIDTH, ARENA_HEIGHT).into(),
                ..Default::default()
            }),
            ..Default::default()
        }))
        .insert_resource(ClearColor(Color::srgb(0., 0., 0.)))
        .insert_resource(Score { left: 0, right: 0 })
        .add_systems(Startup, setup_system)
        .add_systems(
            Update,
            (
                move_player_system,
                move_ball_system,
                bounce_ball_system,
                update_score_system,
                pause_background_music_system,
            ),
        )
        .run();
}

/*
* A resource is a global location that provides access to some information or service for
* the entire Bevy app, and in addition to using pre-made Bevy resources you can create your own.

* The AssetServer acts as a single location in which to store loaded assets like sprites,
* so they can be easily retrieved and used by multiple components without having to load them
* into memory multiple times.
*/
fn setup_system(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
    mut texture_atlases: ResMut<Assets<TextureAtlasLayout>>,
) {
    commands.spawn((
        Camera2d,
        // The camera itself is centered at the middle of the arena at unit height (z-parameter) above the canvas
        Transform::from_xyz(ARENA_WIDTH / 2., ARENA_HEIGHT / 2., 1.),
    ));

    // spawn background music
    commands.spawn((
        AudioPlayer::new(asset_server.load(BACKGROUND_AUDIO_PATH)),
        PlaybackSettings::LOOP.with_volume(Volume::Linear(0.25)),
        BackgroundMusic,
    ));

    /*
     * Usually, using an individual image for each thing on the screen is too inefficient for a game
     * because the image (texture) needs to be loaded into the graphics processing unit (GPU),
     * which has a high overhead. We usually aggregate all the images (or some of the related ones)
     * into a big picture called the “spritesheet.” Then we “cut out” a small section of the big image
     * for each item. This way, we reduce the overall loading time and allow the GPU to handle
     * the images more efficiently.
     */
    let sprite_sheet_handle = asset_server.load(SPRITES_SHEET_PATH);
    let mut sprite_layout = TextureAtlasLayout::new_empty(SPRITES_SHEET_SIZE);

    /*
     * To get individual sprites from the atlas we generate the coordinates of rectangles
     * encompassing each sprite (these rectangles are defined by the upper left and lower right
     * points in pixels on the spritesheet).
     *
     * For images the (0,0) coordinate is in the top left.
     */
    let left_cat_index = sprite_layout.add_texture(URect::from_corners(
        LEFT_CAT_TEXTURE_CORNER,
        LEFT_CAT_TEXTURE_CORNER + CAT_SIZE,
    ));
    let right_cat_index = sprite_layout.add_texture(URect::from_corners(
        RIGHT_CAT_TEXTURE_CORNER,
        RIGHT_CAT_TEXTURE_CORNER + CAT_SIZE,
    ));
    let ball_index = sprite_layout.add_texture(URect::from_corners(
        BALL_TEXTURE_CORNER,
        BALL_TEXTURE_CORNER + BALL_SIZE,
    ));

    /*
     * After we’ve added the textures and received the indices for these textures from
     * the atlas layout, we add the new atlas layout into our larger atlas collection and
     * are left with a handle to the asset that can be passed to the player and ball initializers.
     */
    let texture_atlas_layout_handle = texture_atlases.add(sprite_layout);

    spawn_player(
        &mut commands,
        texture_atlas_layout_handle.clone(),
        sprite_sheet_handle.clone(),
        left_cat_index,
        Side::Left,
        PLAYER_WIDTH / 2.,
        PLAYER_HEIGHT / 2.,
    );
    spawn_player(
        &mut commands,
        texture_atlas_layout_handle.clone(),
        sprite_sheet_handle.clone(),
        right_cat_index,
        Side::Right,
        ARENA_WIDTH - PLAYER_WIDTH / 2.,
        PLAYER_HEIGHT / 2.,
    );

    let bounce_sound = asset_server.load(BOUNCE_AUDIO_PATH);
    let score_sound = asset_server.load(SCORE_AUDIO_PATH);
    spawn_ball(
        &mut commands,
        texture_atlas_layout_handle.clone(),
        sprite_sheet_handle.clone(),
        ball_index,
        bounce_sound,
        score_sound,
    );

    let score_font_handle = asset_server.load(SCORE_FONT_PATH);
    spawn_scoreboard(
        &mut commands,
        score_font_handle.clone(),
        Side::Left,
        SCORE_BOARD_LEFT_X,
    );
    spawn_scoreboard(
        &mut commands,
        score_font_handle.clone(),
        Side::Right,
        SCORE_BOARD_RIGHT_X,
    );
}
