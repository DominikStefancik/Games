use bevy::math::Vec2;

pub const UPGRADE_TEXTURE_SIZE: Vec2 = Vec2::new(64., 64.);
pub const UPGRADE_MOVEMENT_SPEED: f32 = 10.;

#[derive(Clone, Copy)]
pub enum UpgradeType {
    Heart,
    Laser,
    Size,
    Speed,
}

impl UpgradeType {
    pub fn all_variants_array() -> [UpgradeType; 4] {
        [
            UpgradeType::Heart,
            UpgradeType::Laser,
            UpgradeType::Size,
            UpgradeType::Speed,
        ]
    }
}
