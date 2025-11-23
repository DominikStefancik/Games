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

impl Animation {
    pub fn new(first_frame: usize, last_frame: usize) -> Self {
        Animation {
            first_frame,
            last_frame,
        }
    }
}

#[derive(Component, Deref, DerefMut)]
pub struct AnimationTimer(pub Timer);
