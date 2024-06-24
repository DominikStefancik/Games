use crate::constants::{ARENA_WIDTH, PLAYER_WIDTH};
use bevy::prelude::{AudioSource, Component, Handle, KeyCode, Vec2};

#[derive(Clone, Copy)]
pub enum Side {
    Left,
    Right,
}

impl Side {
    // determines which keyboard keys move the left/right cat to the left
    pub fn move_cat_left_key(&self) -> KeyCode {
        match self {
            Side::Left => KeyCode::KeyA,
            Side::Right => KeyCode::ArrowLeft,
        }
    }

    // determines which keyboard keys move the left/right cat to the right
    pub fn move_cat_right_key(&self) -> KeyCode {
        match self {
            Side::Left => KeyCode::KeyD,
            Side::Right => KeyCode::ArrowRight,
        }
    }

    // determines borders of an area in which the left/right cat can move
    pub fn cat_movement_range(&self) -> (f32, f32) {
        match self {
            Side::Left => (PLAYER_WIDTH / 2., ARENA_WIDTH / 2. - PLAYER_WIDTH / 2.),
            Side::Right => (
                ARENA_WIDTH / 2. + PLAYER_WIDTH / 2.,
                ARENA_WIDTH - PLAYER_WIDTH / 2.,
            ),
        }
    }
}

#[derive(Component)]
pub struct Player {
    pub side: Side,
}

#[derive(Component)]
pub struct Ball {
    pub radius: f32,
    pub velocity: Vec2,
    pub bounce_sound: Handle<AudioSource>,
    pub score_sound: Handle<AudioSource>,
}

#[derive(Component)]
pub struct ScoreBoard {
    pub side: Side,
}

// Marker component for our BackgroundMusic entity
#[derive(Component)]
pub struct BackgroundMusic;

// Marker component for our Sound entity
#[derive(Component)]
pub struct Sound;
