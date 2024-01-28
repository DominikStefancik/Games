use bevy::prelude::*;

// represents the player
// it is called Stack component because it's a component which doesn't contain any data
#[derive(Component)]
pub struct Paddle;

// represents the ball
#[derive(Component)]
pub struct Ball {
    // this property is used to calculate a possible collision with other objects
    pub size: Vec2,
}

// represents the ball's velocity
#[derive(Component, Deref, DerefMut)]
pub struct BallVelocity(pub Vec2);

// represents any object the ball can collide with (basically touch it), e.g. wall, paddle, brick
#[derive(Component)]
pub struct Collider {
    // this property is used to calculate a possible collision with the ball
    pub size: Vec2,
}

// represents the wall
#[derive(Bundle)]
pub struct WallBundle {
    pub sprite_bundle: SpriteBundle,
    pub collider: Collider,
}
