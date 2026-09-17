use bevy::{asset::Handle, audio::AudioSource, ecs::resource::Resource, image::Image};
use rand::rngs::StdRng;

use crate::plugins::{BrickType, UpgradeType};

#[derive(Clone)]
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

#[derive(Clone)]
pub struct UpgradeTexture {
    pub heart: Handle<Image>,
    pub laser: Handle<Image>,
    pub size: Handle<Image>,
    pub speed: Handle<Image>,
}

#[derive(Resource)]
pub struct GameTexture {
    pub background: Handle<Image>,
    pub ball: Handle<Image>,
    pub paddle: BoxTexture,
    pub blue_brick: BoxTexture,
    pub bronze_brick: BoxTexture,
    pub green_brick: BoxTexture,
    pub grey_brick: BoxTexture,
    pub orange_brick: BoxTexture,
    pub purple_brick: BoxTexture,
    pub red_brick: BoxTexture,
    pub upgrade: UpgradeTexture,
    pub heart: Handle<Image>,
    pub laser: Handle<Image>,
    pub projectile: Handle<Image>,
}

impl GameTexture {
    /*
     * We return reference instead of value.
     * The reason is 9 Arc clone/drop pairs per call. The system spawn_bricks calls it once per brick ->
     * ~650 atomic refcount ops per level load, plus once per brick hit.
     */
    pub fn get_brick_texture(&self, brick_type: BrickType) -> &BoxTexture {
        match brick_type {
            BrickType::Blue => &self.blue_brick,
            BrickType::Bronze => &self.bronze_brick,
            BrickType::Green => &self.green_brick,
            BrickType::Grey => &self.grey_brick,
            BrickType::Orange => &self.orange_brick,
            BrickType::Purple => &self.purple_brick,
            BrickType::Red => &self.red_brick,
        }
    }

    pub fn get_upgrade_texture(&self, upgrade_type: UpgradeType) -> Handle<Image> {
        match upgrade_type {
            UpgradeType::Heart => self.upgrade.heart.clone(),
            UpgradeType::Laser => self.upgrade.laser.clone(),
            UpgradeType::Size => self.upgrade.size.clone(),
            UpgradeType::Speed => self.upgrade.speed.clone(),
        }
    }
}

#[derive(Resource)]
pub struct GameSound {
    pub background_music: Handle<AudioSource>,
    pub ball_impact: Handle<AudioSource>,
    pub ball_fall: Handle<AudioSource>,
    pub laser_shot: Handle<AudioSource>,
    pub laser_hit: Handle<AudioSource>,
    pub upgrade: Handle<AudioSource>,
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
