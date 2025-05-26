use bevy::{
    image::TextureAtlasLayout,
    prelude::{Handle, Image, Resource},
};

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
    pub explosion: Handle<Image>,
    pub explosion_atlas: Handle<TextureAtlasLayout>,
}

pub const ENEMY_COUNT_MAX: u8 = 3;

#[derive(Resource)]
pub struct EnemyCount(pub u8);

#[derive(Resource)]
pub struct PlayerState {
    pub is_on_stage: bool, // is player alive
    pub last_shot: f64,    // by convention the value -1 represents no shot
}

impl Default for PlayerState {
    fn default() -> Self {
        Self {
            is_on_stage: false,
            last_shot: -1.,
        }
    }
}

impl PlayerState {
    pub fn player_shot(&mut self, time: f64) {
        self.is_on_stage = false;
        self.last_shot = time
    }

    pub fn player_spawned(&mut self) {
        self.is_on_stage = true;
        self.last_shot = -1.;
    }
}
