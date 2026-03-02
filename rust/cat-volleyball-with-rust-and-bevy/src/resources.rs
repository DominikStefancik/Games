use bevy::prelude::Resource;

#[derive(Resource)]
pub struct Score {
    pub left: u16,
    pub right: u16,
}
