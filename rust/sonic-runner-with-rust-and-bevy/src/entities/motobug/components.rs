use bevy::{ecs::component::Component, math::primitives::Rectangle};

use crate::entities::components::ColliderHitBox;

pub const MOTOBUG_SPRITE_FRAME_SIZE: (f32, f32) = (48., 30.);
pub const MOTOBUG_SPRITE_SCALE: f32 = 3.;
const MOTOBUG_COLLIDER_SHAPE: Rectangle = Rectangle::new(
    MOTOBUG_SPRITE_FRAME_SIZE.0 * MOTOBUG_SPRITE_SCALE,
    MOTOBUG_SPRITE_FRAME_SIZE.1 * MOTOBUG_SPRITE_SCALE,
);

#[derive(Component)]
#[require(ColliderHitBox = ColliderHitBox(MOTOBUG_COLLIDER_SHAPE))]
pub struct Motobug;
