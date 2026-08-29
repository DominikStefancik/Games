use bevy::ecs::component::Component;

#[derive(Component)]
pub struct Paddle {
    pub direction: f32,
    pub speed: f32,
}
