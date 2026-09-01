use bevy::math::bounding::{Aabb2d, IntersectsVolume};

pub fn detect_upgrade_collision(
    upgrade_bounding_rectangle: Aabb2d,
    paddle_bounding_rectangle: Aabb2d,
) -> bool {
    upgrade_bounding_rectangle.intersects(&paddle_bounding_rectangle)
}
