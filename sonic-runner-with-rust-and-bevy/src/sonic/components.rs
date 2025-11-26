use bevy::{ecs::component::Component, math::primitives::Rectangle};

use crate::entities::components::ColliderHitBox;

pub const SONIC_SPRITE_FRAME_SIZE: (f32, f32) = (32., 44.);
pub const SONIC_SPRITE_SCALE: f32 = 3.;
const SONIC_COLLIDER_SHAPE: Rectangle = Rectangle::new(
    SONIC_SPRITE_FRAME_SIZE.0 * SONIC_SPRITE_SCALE,
    SONIC_SPRITE_FRAME_SIZE.1 * SONIC_SPRITE_SCALE,
);

#[derive(Component)]
#[require(ColliderHitBox = ColliderHitBox(SONIC_COLLIDER_SHAPE))]
pub struct Sonic;
