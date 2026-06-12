use bevy::{camera::Camera2d, ecs::system::Commands};

pub fn spawn_camera(mut commands: Commands) {
    commands.spawn(Camera2d);
}
