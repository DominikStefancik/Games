use crate::components::{Player, Side};
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
