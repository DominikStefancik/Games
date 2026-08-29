use bevy::{asset::Handle, ecs::resource::Resource, image::Image};
use rand::rngs::StdRng;

#[derive(Resource)]
pub struct GameTexture {
    pub background: Handle<Image>,
    pub ball: Handle<Image>,
}

#[derive(Resource)]
pub struct Randomizer {
    pub rng: StdRng,
}

impl Randomizer {
    pub fn new() -> Self {
        Randomizer {
            rng: rand::make_rng(),
        }
    }
}
