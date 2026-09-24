use bevy::{
    ecs::resource::Resource,
    prelude::{Deref, DerefMut},
    time::Timer,
};

#[derive(Resource, Deref, DerefMut)]
pub struct PlayAgainCooldownTimer(pub Timer);
