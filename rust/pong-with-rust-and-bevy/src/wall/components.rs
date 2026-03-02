use bevy::{color::Color, ecs::component::Component};

use crate::{collision::Collider, components::Position};

pub const WALL_COLOR: Color = Color::srgb(0., 0., 1.);
pub const WALL_HEIGHT: f32 = 20.;

/*
 * We need something to mark our entity is a wall, rather than a paddle or a ball.
 * For this component, it's enough to just have it on our entity. It doesn't need any data.
 * When you use a component in this way its called a "marker component".
 */
#[derive(Component)]
/*
 * By adding a require macro to our ball we are telling Bevy that any entity with a Ball should also be spawned
 * with a Position and Collider.
 * So long as our Position has a default trait implemented, it will add that default if we do not add our own.
 * We don't give our wall's collider a default shape, because it will depend in the window's size, which we will
 * figure out when spwaning the wall.
 */
#[require(Position, Collider)]
pub struct Wall;
