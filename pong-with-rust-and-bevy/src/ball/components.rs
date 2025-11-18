use bevy::{
    color::Color,
    ecs::component::Component,
    math::{
        Vec2,
        primitives::{Circle, Rectangle},
    },
};

use crate::components::Position;
use crate::{collision::Collider, components::Velocity};

const BALL_RADIUS: f32 = 10.;
pub const BALL_SHAPE: Circle = Circle::new(BALL_RADIUS);
pub const BALL_COLOR: Color = Color::srgb(1., 0., 0.);
pub const BALL_SPEED: f32 = 1.5;

/*
 * We need something to mark our entity is a ball, rather than a wall or a paddle.
 * For this component, it's enough to just have it on our entity. It doesn't need any data.
 * When you use a component in this way its called a "marker component".
 */
#[derive(Component)]
/*
 * By adding a require macro to our ball we are telling Bevy that any entity with a Ball should also be spawned
 * with a Position, Velocity and Collider.
 * So long as our Position has a default trait implemented, it will add that default if we do not add our own.
 * We give our ball a Velocity with a different default that wasn't 0 so that our ball actually moves
 * when its first spawned.
 */
#[require(Position, Velocity = Velocity(Vec2::new(-BALL_SPEED, BALL_SPEED)), Collider = Collider(Rectangle::new(BALL_RADIUS, BALL_RADIUS)))]
pub struct Ball;
