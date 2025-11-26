use bevy::{
    ecs::component::Component,
    prelude::{Deref, DerefMut},
    time::Timer,
};

#[derive(Component)]
pub struct Scrollable {
    pub pixels_to_scroll: f32,
}

impl Scrollable {
    pub fn new(pixels_to_scroll: f32) -> Self {
        Scrollable { pixels_to_scroll }
    }
}

#[derive(Component, Deref, DerefMut)]
pub struct ScrollingTimer(pub Timer);

#[derive(Component)]
pub struct Background;

#[derive(Component)]
pub struct Platform;
