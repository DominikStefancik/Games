use bevy::{asset::Handle, ecs::resource::Resource, image::Image};
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
    pub fn get_brick_texture(&self, brick_type: BrickType) -> BoxTexture {
        match brick_type {
            BrickType::Blue => self.blue_brick.clone(),
            BrickType::Bronze => self.bronze_brick.clone(),
            BrickType::Green => self.green_brick.clone(),
            BrickType::Grey => self.grey_brick.clone(),
            BrickType::Orange => self.orange_brick.clone(),
            BrickType::Purple => self.purple_brick.clone(),
            BrickType::Red => self.red_brick.clone(),
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
