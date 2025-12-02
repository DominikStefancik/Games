use bevy::{
    asset::Handle,
    audio::AudioSource,
    ecs::resource::Resource,
    image::{Image, TextureAtlasLayout},
    text::Font,
};

#[derive(Resource)]
pub struct GameTextures {
    pub background: Handle<Image>,
    pub platforms: Handle<Image>,
    pub sonic: Handle<Image>,
    pub sonic_atlas: Handle<TextureAtlasLayout>,
    pub ring: Handle<Image>,
    pub ring_atlas: Handle<TextureAtlasLayout>,
}

#[derive(Resource)]
pub struct GameSounds {
    pub background: Handle<AudioSource>,
    pub ring: Handle<AudioSource>,
    pub jump: Handle<AudioSource>,
}

#[derive(Resource)]
pub struct GameFonts {
    pub mania: Handle<Font>,
}

#[derive(Resource)]
pub struct GameSettings {
    pub speed: f32,
    pub score: u32,
    pub score_multiplier: u8,
    pub best_score: u32,
}

const INITIAL_SPEED: f32 = 10.;

impl GameSettings {
    pub fn new() -> Self {
        GameSettings {
            speed: INITIAL_SPEED,
            score: 0,
            score_multiplier: 0,
            best_score: 0,
        }
    }

    pub fn increase_score(&mut self, score_increment: u32) {
        self.score += score_increment;
    }

    pub fn increase_speed(&mut self, speed_increment: f32) {
        self.speed += speed_increment;
    }

    pub fn increase_score_multiplier(&mut self) {
        self.score_multiplier += 1;
    }

    pub fn reset_score_multiplier(&mut self) {
        self.score_multiplier = 0;
    }

    pub fn reset(&mut self) {
        self.speed = INITIAL_SPEED;
        self.score = 0;
        self.score_multiplier = 0;
    }
}
