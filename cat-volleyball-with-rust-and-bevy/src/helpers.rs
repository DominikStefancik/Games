use crate::components::{Ball, Player, Side};
use crate::constants::{ARENA_HEIGHT, ARENA_WIDTH, BALL_RADIUS, BALL_VELOCITY};
use bevy::prelude::{
    Commands, Handle, SpriteSheetBundle, TextureAtlas, TextureAtlasSprite, Transform,
};

pub fn spawn_player(
    commands: &mut Commands,
    // The TextureAtlas is a single location where we can store all texture atlases in the whole program
    atlas: Handle<TextureAtlas>,
    cat_sprite_index: usize,
    side: Side,
    x: f32,
    y: f32,
) {
    commands.spawn((
        SpriteSheetBundle {
            sprite: TextureAtlasSprite::new(cat_sprite_index),
            texture_atlas: atlas,
            transform: Transform::from_xyz(x, y, 0.),
            ..Default::default()
        },
        Player { side },
    ));
}

pub fn spawn_ball(
    commands: &mut Commands,
    // The TextureAtlas is a single location where we can store all texture atlases in the whole program
    atlas: Handle<TextureAtlas>,
    ball_sprite_index: usize,
) {
    commands.spawn((
        SpriteSheetBundle {
            sprite: TextureAtlasSprite::new(ball_sprite_index),
            texture_atlas: atlas,
            transform: Transform::from_xyz(ARENA_WIDTH / 2., ARENA_HEIGHT / 2., 0.),
            ..Default::default()
        },
        Ball {
            radius: BALL_RADIUS,
            velocity: BALL_VELOCITY,
        },
    ));
}
