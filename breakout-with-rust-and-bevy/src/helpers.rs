use crate::components::{Ball, BallVelocity, Collider, Paddle, WallBundle};
use crate::constants::{
    BALL_COLOR, BALL_INITIAL_DIRECTION, BALL_RADIUS, BALL_SPEED, BALL_STARTING_POSITION,
    BOTTOM_WALL, LEFT_WALL, PADDLE_COLOR, PADDLE_SIZE, PADDLE_START_Y, RIGHT_WALL, TOP_WALL,
    WALL_BLOCK_HEIGHT, WALL_BLOCK_WIDTH, WALL_COLOR, WALL_THICKNESS,
};
use bevy::asset::Assets;
use bevy::math::{vec2, vec3};
use bevy::prelude::*;
use bevy::sprite::MaterialMesh2dBundle;

pub fn spawn_player(commands: &mut Commands) {
    commands.spawn((
        SpriteBundle {
            transform: Transform {
                translation: Vec3::new(0., PADDLE_START_Y, 0.),
                ..Default::default()
            },
            sprite: Sprite {
                color: PADDLE_COLOR,
                custom_size: Some(PADDLE_SIZE),
                ..Default::default()
            },
            ..Default::default()
        },
        Paddle,
        // the Collider component is necessary if we want the ball to collide with the paddle
        Collider { size: PADDLE_SIZE },
    ));
}

pub fn spawn_ball(
    commands: &mut Commands,
    mut meshes: ResMut<Assets<Mesh>>,
    mut materials: ResMut<Assets<ColorMaterial>>,
) {
    commands.spawn((
        MaterialMesh2dBundle {
            mesh: meshes.add(shape::Circle::new(BALL_RADIUS).into()).into(),
            material: materials.add(ColorMaterial::from(BALL_COLOR)),
            transform: Transform {
                translation: BALL_STARTING_POSITION,
                ..Default::default()
            },
            ..default()
        },
        Ball {
            // add a small offset number to make collisions a bit nicer
            size: vec2(BALL_RADIUS + 5., BALL_RADIUS + 5.),
        },
        BallVelocity(BALL_SPEED * BALL_INITIAL_DIRECTION),
    ));
}

pub fn spawn_wall(commands: &mut Commands) {
    let vertical_wall_size = vec2(WALL_THICKNESS, WALL_BLOCK_HEIGHT + WALL_THICKNESS);
    let horizontal_wall_size = vec2(WALL_BLOCK_WIDTH + WALL_THICKNESS, WALL_THICKNESS);

    // left wall
    commands.spawn(create_wall_bundle(LEFT_WALL, 0., vertical_wall_size));
    // right wall
    commands.spawn(create_wall_bundle(RIGHT_WALL, 0., vertical_wall_size));
    // top wall
    commands.spawn(create_wall_bundle(0., TOP_WALL, horizontal_wall_size));
    // right wall
    commands.spawn(create_wall_bundle(0., BOTTOM_WALL, horizontal_wall_size));
}

fn create_wall_bundle(x: f32, y: f32, wall_size: Vec2) -> WallBundle {
    WallBundle {
        sprite_bundle: SpriteBundle {
            transform: Transform {
                translation: vec3(x, y, 0.),
                ..Default::default()
            },
            sprite: Sprite {
                color: WALL_COLOR,
                custom_size: Some(wall_size),
                ..Default::default()
            },
            ..Default::default()
        },
        collider: Collider { size: wall_size },
    }
}
