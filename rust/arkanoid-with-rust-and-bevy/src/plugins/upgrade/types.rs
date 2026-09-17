#[derive(Clone, Copy, Debug)]
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
