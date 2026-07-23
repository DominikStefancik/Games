use bevy::ecs::resource::Resource;

#[derive(Resource, Debug, Default)]
pub struct Score {
    pub current: u32,
    pub best: u32,
}
