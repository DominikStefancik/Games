use bevy::{
    asset::Handle,
    audio::AudioSource,
    ecs::resource::Resource,
    image::{Image, TextureAtlasLayout},
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
}
