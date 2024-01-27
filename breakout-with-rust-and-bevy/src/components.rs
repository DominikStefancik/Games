use bevy::prelude::{Component, Deref, DerefMut, Vec2};

// represents the player
// it is called Stack component because it's a component which doesn't contain any data
#[derive(Component)]
pub struct Paddle;

// represents the ball
#[derive(Component)]
pub struct Ball;

// represents the ball's velocity
#[derive(Component, Deref, DerefMut)]
pub struct BallVelocity(pub Vec2);
