use crate::components::{Ball, BallVelocity, Brick, Collider, Paddle, ScoreBoardText, WallBundle};
use crate::constants::{
    BALL_COLOR, BALL_INITIAL_DIRECTION, BALL_RADIUS, BALL_SPEED, BALL_STARTING_POSITION,
    BOTTOM_WALL, BRICK_COLOR, BRICK_SIZE, GAP_BETWEEN_BRICKS, GAP_BETWEEN_BRICKS_AND_CEILING,
    GAP_BETWEEN_BRICKS_AND_SIDES, GAP_BETWEEN_PADDLE_AND_BRICKS, LEFT_WALL, PADDLE_COLOR,
    PADDLE_SIZE, PADDLE_START_Y, RIGHT_WALL, SCOREBOARD_FONT_SIZE, SCOREBOARD_SCORE_COLOR,
    SCOREBOARD_TEXT_COLOR, SCOREBOARD_TEXT_PADDING, TOP_WALL, WALL_BLOCK_HEIGHT, WALL_BLOCK_WIDTH,
    WALL_COLOR, WALL_THICKNESS,
};
use bevy::prelude::{
    children, vec2, vec3, Assets, Circle, ColorMaterial, Commands, Mesh, Mesh2d, MeshMaterial2d,
    Node, PositionType, ResMut, SpawnRelated, Sprite, Text, TextColor, TextFont, TextSpan,
    Transform, Vec2, Vec3,
};

pub fn spawn_player(commands: &mut Commands) {
    commands.spawn((
        Sprite {
            color: PADDLE_COLOR,
            custom_size: Some(PADDLE_SIZE),
            ..Default::default()
        },
        Transform {
            translation: Vec3::new(0., PADDLE_START_Y, 0.),
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
        Mesh2d(meshes.add(Circle::new(BALL_RADIUS))),
        MeshMaterial2d(materials.add(ColorMaterial::from(BALL_COLOR))),
        Transform::from_translation(BALL_STARTING_POSITION),
        Ball {
            // add a small offset number to make collisions a bit nicer
            diameter: (BALL_RADIUS + 5.) * 2.,
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
        sprite: Sprite::from_color(WALL_COLOR, wall_size),
        transform: Transform::from_translation(vec3(x, y, 0.)),
        collider: Collider { size: wall_size },
    }
}

pub fn spawn_bricks(commands: &mut Commands) {
    let offset_x = LEFT_WALL + GAP_BETWEEN_BRICKS_AND_SIDES + BRICK_SIZE.x / 2.;
    let offset_y = BOTTOM_WALL + GAP_BETWEEN_PADDLE_AND_BRICKS + BRICK_SIZE.y / 2.;

    let bricks_total_width = (RIGHT_WALL - LEFT_WALL) - GAP_BETWEEN_BRICKS_AND_SIDES * 2.;
    let bricks_total_height =
        (TOP_WALL - BOTTOM_WALL) - GAP_BETWEEN_BRICKS_AND_CEILING - GAP_BETWEEN_PADDLE_AND_BRICKS;

    let rows = (bricks_total_height / (BRICK_SIZE.y + GAP_BETWEEN_BRICKS)).floor() as u32;
    let columns = (bricks_total_width / (BRICK_SIZE.x + GAP_BETWEEN_BRICKS)).floor() as u32;

    for row in 0..rows {
        for column in 0..columns {
            let brick_position = vec2(
                offset_x + column as f32 * (BRICK_SIZE.x + GAP_BETWEEN_BRICKS),
                offset_y + row as f32 * (BRICK_SIZE.y + GAP_BETWEEN_BRICKS),
            );

            commands.spawn((
                Sprite::from_color(BRICK_COLOR, BRICK_SIZE),
                Transform::from_translation(brick_position.extend(0.0)),
                Brick,
                // the Collider component is necessary if we want the ball to collide with a brick
                Collider { size: BRICK_SIZE },
            ));
        }
    }
}

pub fn spawn_scoreboard(commands: &mut Commands) {
    commands.spawn((
        Text::new("Score: "),
        TextFont::from_font_size(SCOREBOARD_FONT_SIZE),
        TextColor::from(SCOREBOARD_TEXT_COLOR),
        // the Node tells Bevy how to position a text
        Node {
            position_type: PositionType::Absolute,
            top: SCOREBOARD_TEXT_PADDING,
            left: SCOREBOARD_TEXT_PADDING,
            ..Default::default()
        },
        ScoreBoardText,
        // children texts of the score text
        // if we want to use the macro children! we have to import SpawnRelated
        children![(
            TextSpan::default(),
            TextFont::from_font_size(SCOREBOARD_FONT_SIZE),
            TextColor::from(SCOREBOARD_SCORE_COLOR)
        )],
    ));
}
