use bevy::ecs::resource::Resource;

use crate::plugins::LEVEL_1_MAP;

#[derive(Resource)]
pub struct LevelInfo {
    pub current_level: u16,
    pub level_map: Vec<&'static str>,
}

impl LevelInfo {
    pub fn init() -> Self {
        LevelInfo {
            current_level: 1,
            level_map: LEVEL_1_MAP.to_vec(),
        }
    }
}
