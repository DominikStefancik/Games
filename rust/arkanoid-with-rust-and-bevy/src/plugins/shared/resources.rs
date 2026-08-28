use bevy::{asset::Handle, ecs::resource::Resource, image::Image};

#[derive(Resource)]
pub struct GameTexture {
    pub background: Handle<Image>,
}
