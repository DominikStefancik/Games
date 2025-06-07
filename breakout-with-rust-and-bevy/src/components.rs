use bevy::{
    prelude::{Bundle, Component, Deref, DerefMut, Vec2},
    sprite::Sprite,
    transform::components::Transform,
};

// represents the player
// it is called Stack component because it's a component which doesn't contain any data
#[derive(Component)]
pub struct Paddle;

// represents the ball
#[derive(Component)]
pub struct Ball {
    // this property is used to calculate a possible collision with other objects
    pub diameter: f32,
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
    pub sprite: Sprite,
    pub transform: Transform,
    pub collider: Collider,
}

// represents a single brick
// it is called Stack component because it's a component which doesn't contain any data
#[derive(Component)]
pub struct Brick;

// represents a text on the scoreboard
#[derive(Component)]
pub struct ScoreBoardText;
