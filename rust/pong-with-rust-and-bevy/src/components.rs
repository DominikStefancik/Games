use bevy::{ecs::component::Component, math::Vec2, prelude::Transform};

/*
 * By creating a component, we essentially made a new optional column, like in a database table, on any entity.
 * When we insert this onto an entity we are filling in the value of that column for that particular row.
 *
 * You have your "logical position" which is our position in the game world. This would be the same no matter how big
 * your monitor was.
 * Then we have our "physical position" which is where you are on the rendered window and would change depending on
 * your display settings.
 *
 * If we want the screen to be resizable we don't want to mix our logical position with the physical position of where
 * it will be rendered on the screen.
 *
 * A better alternative is to use a separate Position that we control ourselves, and then we can project that position
 * onto the transform in a single separate system.
 *
 */
#[derive(Component, Default)]
#[require(Transform)]
pub struct Position(pub Vec2);

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

#[derive(Component)]
pub struct HumanPlayer;

#[derive(Component)]
pub struct AiPlayer;
