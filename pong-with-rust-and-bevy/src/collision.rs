/*
 * "Aabb2d" represents a bounding box for gutters, paddles or ball.
 * The other two types "BoundingVolume" and "IntersectsVolume" are traits that won't be used directly
 * but are implemented in the first two types and will need to be in scope.
 */
use bevy::{
    ecs::{
        component::Component,
        query::{With, Without},
        system::{Query, Single},
    },
    math::{
        Vec2,
        bounding::{Aabb2d, BoundingVolume, IntersectsVolume},
        primitives::Rectangle,
    },
};

use crate::{
    ball::components::{Ball, Velocity},
    components::Position,
};

#[derive(Debug, PartialEq, Eq, Clone, Copy)]
pub enum Collision {
    Left,
    Right,
    Top,
    Bottom,
}

#[derive(Component, Default)]
pub struct Collider(pub Rectangle);

impl Collider {
    fn half_size(&self) -> Vec2 {
        self.0.half_size
    }
}

/*
 * We know there is only one game object with a component Ball, so we use Single type to find it
 * But there can be more than on objects with the components Position and Collider, so we use Query.
 *
 */
pub fn handle_collisions_system(
    ball: Single<(&mut Velocity, &Position, &Collider), With<Ball>>,
    other_objects: Query<(&Position, &Collider), Without<Ball>>,
) {
    let (mut ball_velocity, ball_position, ball_collider) = ball.into_inner();

    for (other_position, other_collider) in &other_objects {
        if let Some(collision) = collide_with_side(
            Aabb2d::new(ball_position.0, ball_collider.half_size()),
            Aabb2d::new(other_position.0, other_collider.half_size()),
        ) {
            match collision {
                Collision::Left | Collision::Right => ball_velocity.0.x *= -1.,
                Collision::Top | Collision::Bottom => ball_velocity.0.y *= -1.,
            }
        }
    }
}

/*
 * Returns Some if ball collides with wall. The returned Collision is the side of wall that ball hit.
 *
 * The type "Aabb2d" represents a bounding box for gutters, paddles or ball.
 */
fn collide_with_side(ball: Aabb2d, wall: Aabb2d) -> Option<Collision> {
    if !ball.intersects(&wall) {
        return None;
    }

    let closest_point = wall.closest_point(ball.center());
    let offset = ball.center() - closest_point;

    let side = if offset.x.abs() > offset.y.abs() {
        if offset.x < 0. {
            Collision::Left
        } else {
            Collision::Right
        }
    } else if offset.y > 0. {
        Collision::Top
    } else {
        Collision::Bottom
    };

    Some(side)
}
