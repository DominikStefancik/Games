use bevy::prelude::{Handle, Image, Resource, TextureAtlas};

#[derive(Resource)]
pub struct WindowSize {
    pub width: f32,
    pub height: f32,
}

#[derive(Resource)]
pub struct GameTextures {
    pub player: Handle<Image>,
    pub player_laser: Handle<Image>,
    pub enemy: Handle<Image>,
    pub enemy_laser: Handle<Image>,
    // TextureAtlas allows us to navigate through a sheet of pictures
    pub explosion: Handle<TextureAtlas>,
}

pub const ENEMY_COUNT_MAX: u8 = 3;

#[derive(Resource)]
pub struct EnemyCount(pub u8);
