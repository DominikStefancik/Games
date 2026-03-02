use bevy::{
    ecs::component::Component,
    math::primitives::Rectangle,
    prelude::{Deref, DerefMut},
    time::Timer,
};

use crate::entities::components::ColliderHitBox;

pub const SONIC_SPRITE_FRAME_SIZE: (f32, f32) = (32., 44.);
pub const SONIC_SPRITE_SCALE: f32 = 3.;
const SONIC_COLLIDER_SHAPE: Rectangle = Rectangle::new(
    SONIC_SPRITE_FRAME_SIZE.0 * SONIC_SPRITE_SCALE,
    SONIC_SPRITE_FRAME_SIZE.1 * SONIC_SPRITE_SCALE,
);
pub const SONIC_JUMP_MAX_VELOCITY: f32 = 15.;
pub const SONIC_POSITION_MAX_LOW: f32 = -185.;
pub const SONIC_RUN_ANIMATION_DURATION: f32 = 0.04;
pub const SONIC_JUMP_ANIMATION_DURATION: f32 = 0.02;
pub const SONIC_SCORE_FONT_SIZE: f32 = 25.;

#[derive(Component)]
#[require(ColliderHitBox = ColliderHitBox(SONIC_COLLIDER_SHAPE))]
pub struct Sonic {
    pub is_dead: bool,
}

impl Sonic {
    pub fn new() -> Self {
        Sonic { is_dead: false }
    }
}

#[derive(Component)]
pub struct Jump {
    pub is_in_progress: bool,
    pub is_going_down: bool,
    // a jump is "restarted" if Sonic falls down and collides with a motobug
    pub is_restarted: bool,
    pub velocity: f32,
}

impl Jump {
    pub fn new() -> Self {
        Jump {
            is_in_progress: false,
            is_going_down: false,
            is_restarted: false,
            velocity: 0.,
        }
    }
}

pub enum SonicAnimationKind {
    Run,
    Jump,
}

#[derive(Component)]
pub struct SonicScoreTextUi;

#[derive(Component, Deref, DerefMut)]
pub struct SonicScoreTextTimer(pub Timer);
