use bevy::{ecs::component::Component, math::primitives::Rectangle};

use crate::entities::components::ColliderHitBox;

pub const RING_SPRITE_FRAME_SIZE: (f32, f32) = (17., 16.);
pub const RING_SPRITE_SCALE: f32 = 3.;
const RING_COLLIDER_SHAPE: Rectangle = Rectangle::new(
    RING_SPRITE_FRAME_SIZE.0 * RING_SPRITE_SCALE,
    RING_SPRITE_FRAME_SIZE.1 * RING_SPRITE_SCALE,
);

#[derive(Component)]
#[require(ColliderHitBox = ColliderHitBox(RING_COLLIDER_SHAPE))]
pub struct Ring;
