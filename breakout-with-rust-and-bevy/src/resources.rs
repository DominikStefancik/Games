use bevy::prelude::Resource;

// A Resource in Bevy is some data that is unique and is globally accessible

// represents a scoreboard
#[derive(Resource, Clone, Copy)]
pub struct Scoreboard {
    pub score: usize,
}
