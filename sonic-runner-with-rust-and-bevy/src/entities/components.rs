use bevy::{
    ecs::component::Component,
    prelude::{Deref, DerefMut},
    time::Timer,
};

#[derive(Component, Clone, Copy)]
pub struct Animation {
    pub first_frame: usize,
    pub last_frame: usize,
}

#[derive(Component, Deref, DerefMut)]
pub struct AnimationTimer(pub Timer);
