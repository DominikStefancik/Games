mod components;
mod constants;
mod helpers;
mod systems;

use crate::components::Side;
use crate::constants::{
    ARENA_HEIGHT, ARENA_WIDTH, BALL_SIZE, BALL_TEXTURE_CORNER, CAT_SIZE, LEFT_CAT_TEXTURE_CORNER,
    PLAYER_HEIGHT, PLAYER_WIDTH, RIGHT_CAT_TEXTURE_CORNER, SPRITE_SHEET_SIZE,
};
use crate::helpers::{spawn_ball, spawn_player};
use crate::systems::move_player_system;
use bevy::prelude::*;

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
        .insert_resource(ClearColor(Color::rgb(0., 0., 0.)))
        .add_systems(Startup, setup_system)
        .add_systems(Update, (bevy::window::close_on_esc, move_player_system))
        .run()
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
    mut texture_atlas: ResMut<Assets<TextureAtlas>>,
) {
    commands.spawn(Camera2dBundle {
        // The camera itself is centered at the middle of the arena at unit height (z-parameter) above the canvas
        transform: Transform::from_xyz(ARENA_WIDTH / 2., ARENA_HEIGHT / 2., 1.),
        ..Default::default()
    });

    /*
     * Usually, using an individual image for each thing on the screen is too inefficient for a game
     * because the image (texture) needs to be loaded into the graphics processing unit (GPU),
     * which has a high overhead. We usually aggregate all the images (or some of the related ones)
     * into a big picture called the “spritesheet.” Then we “cut out” a small section of the big image
     * for each item. This way, we reduce the overall loading time and allow the GPU to handle
     * the images more efficiently.
     */
    let spritesheet = asset_server.load("textures/spritesheet.png");
    let mut sprite_atlas = TextureAtlas::new_empty(spritesheet, SPRITE_SHEET_SIZE);

    /*
     * To get individual sprites from the atlas we generate the coordinates of rectangles
     * encompassing each sprite (these rectangles are defined by the upper left and lower right
     * points in pixels on the spritesheet).
     *
     * For images the (0,0) coordinate is in the top left.
     */
    let left_cat_index = sprite_atlas.add_texture(Rect::from_corners(
        LEFT_CAT_TEXTURE_CORNER,
        LEFT_CAT_TEXTURE_CORNER + CAT_SIZE,
    ));
    let right_cat_index = sprite_atlas.add_texture(Rect::from_corners(
        RIGHT_CAT_TEXTURE_CORNER,
        RIGHT_CAT_TEXTURE_CORNER + CAT_SIZE,
    ));
    let ball_index = sprite_atlas.add_texture(Rect::from_corners(
        BALL_TEXTURE_CORNER,
        BALL_TEXTURE_CORNER + BALL_SIZE,
    ));

    /*
     * After we’ve added the textures and received the indices for these textures in the atlas,
     * we add the new atlas to our larger atlas collection and are left with a handle to the asset
     * that can be passed to the player initializers.
     */
    let texture_atlas_handle = texture_atlas.add(sprite_atlas);

    spawn_player(
        &mut commands,
        texture_atlas_handle.clone(),
        left_cat_index,
        Side::LEFT,
        PLAYER_WIDTH / 2.,
        PLAYER_HEIGHT / 2.,
    );
    spawn_player(
        &mut commands,
        texture_atlas_handle.clone(),
        right_cat_index,
        Side::RIGHT,
        ARENA_WIDTH - PLAYER_WIDTH / 2.,
        PLAYER_HEIGHT / 2.,
    );
    spawn_ball(&mut commands, texture_atlas_handle.clone(), ball_index);
}
