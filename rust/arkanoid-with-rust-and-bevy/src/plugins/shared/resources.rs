use bevy::{asset::Handle, ecs::resource::Resource, image::Image};
use rand::rngs::StdRng;

pub struct BoxTexture {
    pub bottom: Handle<Image>,
    pub bottom_left: Handle<Image>,
    pub bottom_right: Handle<Image>,
    pub center: Handle<Image>,
    pub left: Handle<Image>,
    pub right: Handle<Image>,
    pub top: Handle<Image>,
    pub top_left: Handle<Image>,
    pub top_right: Handle<Image>,
}

#[derive(Resource)]
pub struct GameTexture {
    pub background: Handle<Image>,
    pub ball: Handle<Image>,
    pub blue_brick: BoxTexture,
    pub bronze_brick: BoxTexture,
    pub green_brick: BoxTexture,
    pub grey_brick: BoxTexture,
    pub orange_brick: BoxTexture,
    pub purple_brick: BoxTexture,
    pub red_brick: BoxTexture,
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
