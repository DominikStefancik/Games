use bevy::{
    ecs::component::Component,
    math::{Vec2, primitives::Rectangle},
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

// represents a hit box (a collision area) of an entity
#[derive(Component)]
pub struct ColliderHitBox(pub Rectangle);

impl ColliderHitBox {
    pub fn half_size(&self) -> Vec2 {
        self.0.half_size
    }
}
