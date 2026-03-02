use bevy::prelude::{AudioSource, Deref, DerefMut, Handle, Resource};

// A Resource in Bevy is some data that is unique and is globally accessible

// represents a scoreboard
#[derive(Resource, Clone, Copy)]
pub struct Scoreboard {
    pub score: usize,
}

#[derive(Resource, Default, Deref, DerefMut)]
pub struct CollisionSound(pub Handle<AudioSource>);
