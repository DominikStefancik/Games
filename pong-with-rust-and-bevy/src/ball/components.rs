use bevy::{
    color::Color,
    ecs::component::Component,
    math::{
        Vec2,
        primitives::{Circle, Rectangle},
    },
};

use crate::collision::Collider;
use crate::components::Position;

const BALL_RADIUS: f32 = 10.;
pub const BALL_SHAPE: Circle = Circle::new(BALL_RADIUS);
pub const BALL_COLOR: Color = Color::srgb(1., 0., 0.);
pub const BALL_SPEED: f32 = 2.;

/*
 * Velocity here is just something we invented, a new component we will make that lets us set a direction we desire to
 * move the next time we do. That way our movement system can just read this value and move the ball.
 *
 * We use velocity to determine where we go with the ball next frame, so the logic for our collision system becomes simple:
 *      If we are colliding on the top or bottom: reverse our y velocity
 *      If we are colliding on the left or right: reverse our x velocity
 *
 * This component is a tuple type, we can access the Vec2 it holds by using the position of the item in the tuple
 * e.g. velocity.0 which would be a Vec2
 */
#[derive(Component, Default)]
pub struct Velocity(pub Vec2);

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
