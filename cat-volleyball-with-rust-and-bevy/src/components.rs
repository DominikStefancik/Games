use crate::constants::{ARENA_WIDTH, PLAYER_WIDTH};
use bevy::prelude::{Component, KeyCode, Vec2};

#[derive(Clone, Copy)]
pub enum Side {
    LEFT,
    RIGHT,
}

impl Side {
    // determines which keyboard keys move the left/right cat to the left
    pub fn move_cat_left_key(&self) -> KeyCode {
        match self {
            Side::LEFT => KeyCode::KeyA,
            Side::RIGHT => KeyCode::ArrowLeft,
        }
    }

    // determines which keyboard keys move the left/right cat to the right
    pub fn move_cat_right_key(&self) -> KeyCode {
        match self {
            Side::LEFT => KeyCode::KeyD,
            Side::RIGHT => KeyCode::ArrowRight,
        }
    }

    // determines borders of an area in which the left/right cat can move
    pub fn cat_movement_range(&self) -> (f32, f32) {
        match self {
            Side::LEFT => (PLAYER_WIDTH / 2., ARENA_WIDTH / 2. - PLAYER_WIDTH / 2.),
            Side::RIGHT => (
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
}
