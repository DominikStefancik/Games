use bevy::{
    asset::Handle,
    audio::AudioSource,
    ecs::resource::Resource,
    image::{Image, TextureAtlasLayout},
    text::Font,
};

const RING_SPEED: f32 = 10.;
const MOTOBUG_INITIAL_SPEED: f32 = 12.;

#[derive(Resource)]
pub struct GameTextures {
    pub background: Handle<Image>,
    pub platforms: Handle<Image>,
    pub sonic: Handle<Image>,
    pub sonic_atlas: Handle<TextureAtlasLayout>,
    pub ring: Handle<Image>,
    pub ring_atlas: Handle<TextureAtlasLayout>,
    pub motobug: Handle<Image>,
    pub motobug_atlas: Handle<TextureAtlasLayout>,
}

#[derive(Resource)]
pub struct GameSounds {
    pub background: Handle<AudioSource>,
    pub ring: Handle<AudioSource>,
    pub jump: Handle<AudioSource>,
    pub destroy: Handle<AudioSource>,
    pub hyper_ring: Handle<AudioSource>,
    pub hurt: Handle<AudioSource>,
}

#[derive(Resource)]
pub struct GameFonts {
    pub mania: Handle<Font>,
}

#[derive(Clone, Copy)]
pub enum RankGrade {
    A,
    B,
    C,
    D,
    E,
    F,
    S,
}

impl From<u32> for RankGrade {
    fn from(value: u32) -> Self {
        match value {
            0..=79 => RankGrade::F,
            80..=99 => RankGrade::E,
            100..=199 => RankGrade::D,
            200..=299 => RankGrade::C,
            300..=399 => RankGrade::B,
            400..=499 => RankGrade::A,
            500..=u32::MAX => RankGrade::S,
        }
    }
}

impl From<RankGrade> for String {
    fn from(value: RankGrade) -> Self {
        match value {
            RankGrade::F => "F".to_string(),
            RankGrade::E => "E".to_string(),
            RankGrade::D => "D".to_string(),
            RankGrade::C => "C".to_string(),
            RankGrade::B => "B".to_string(),
            RankGrade::A => "A".to_string(),
            RankGrade::S => "S".to_string(),
        }
    }
}

#[derive(Resource)]
pub struct GameSettings {
    pub ring_speed: f32,
    pub motobug_speed: f32,
    pub score: u32,
    pub best_score: u32,
    pub score_multiplier: u8,
    pub rank: RankGrade,
    pub best_rank: RankGrade,
}

impl GameSettings {
    pub fn new() -> Self {
        GameSettings {
            ring_speed: 10.,
            motobug_speed: MOTOBUG_INITIAL_SPEED,
            score: 0,
            best_score: 0,
            score_multiplier: 1,
            rank: RankGrade::F,
            best_rank: RankGrade::F,
        }
    }

    pub fn increase_score(&mut self, score_increment: u32) {
        self.score += score_increment;
    }

    pub fn increase_motobug_speed(&mut self, speed_increment: f32) {
        self.motobug_speed += speed_increment;
    }

    pub fn increment_score_multiplier(&mut self) {
        self.score_multiplier += 1;
    }

    pub fn reset_score_multiplier(&mut self) {
        self.score_multiplier = 1;
    }

    pub fn reset(&mut self) {
        self.ring_speed = RING_SPEED;
        self.motobug_speed = MOTOBUG_INITIAL_SPEED;
        self.score = 0;
        self.score_multiplier = 1;
        self.rank = RankGrade::F;
    }
}
