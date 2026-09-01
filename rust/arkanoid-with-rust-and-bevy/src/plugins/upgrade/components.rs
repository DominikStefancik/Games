use bevy::ecs::component::Component;

use crate::plugins::UpgradeType;

#[derive(Component, Debug)]
pub struct Upgrade {
    pub upgrade_type: UpgradeType,
}
