use bevy::prelude::{Handle, Image, Resource};

#[derive(Resource)]
pub struct WindowSize {
    pub width: f32,
    pub height: f32,
}

#[derive(Resource)]
pub struct GameTextures {
    pub player: Handle<Image>,
}
