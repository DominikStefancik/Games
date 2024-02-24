use bevy::prelude::Component;

#[derive(Clone, Copy)]
pub enum Side {
    LEFT,
    RIGHT,
}

#[derive(Component)]
pub struct Player {
    pub side: Side,
}
