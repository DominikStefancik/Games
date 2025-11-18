use bevy::{
    asset::Assets,
    ecs::{
        query::{With, Without},
        system::{Commands, Query, Res, ResMut, Single},
    },
    input::{ButtonInput, keyboard::KeyCode},
    math::{Vec2, bounding::Aabb2d},
    mesh::{Mesh, Mesh2d},
    sprite_render::{ColorMaterial, MeshMaterial2d},
    window::Window,
};

use crate::{
    ball::components::Ball,
    collision::{Collider, Collision, collide_with_wall_side},
    components::{AiPlayer, HumanPlayer, Position, Velocity},
    paddle::components::{PADDLE_COLOR, PADDLE_SHAPE, PADDLE_SPEED, Paddle},
    wall::components::Wall,
};

pub fn spawn_paddles_system(
    mut commands: Commands,
    /*
     * "Resource" is like our components, but doesn't belong to a specific Entity.
     * You can think about them like singleton components.
     * Instead of using a Query for these resources we can ask for them directly as a generic arguments to
     * "Res" or "ResMut".
     *
     * Here we are instructing Bevy:
     * "Give me exclusive mutable access to the resource of type Assets<Mesh>"
     */
    mut meshes: ResMut<Assets<Mesh>>,
    mut materials: ResMut<Assets<ColorMaterial>>,
    /*
     * Bevy adds a Window component to an entity that is representing our real rendered window.
     * This gets added by the DefaultPlugins which loads the WindowPlugin.
     */
    window: Single<&Window>,
) {
    /*
     * When you add assets like a Mesh2d you add them to a resource specific to that asset type. So all Mesh2d
     * are stored in our Assets<Mesh2d> for example. We will add them and Bevy will return you a Handle to that asset.
     *
     * A Handle is just like an Entity. It's a unique ID for an asset we have loaded. So a Mesh2d is not actually
     * asking us for the whole mesh. It really just wants the unique ID of that mesh that gets stored in an Assets<T>.
     *
     * "Assets::add" will load these into memory and return a Handle (an ID) to these assets.
     * When all references to this Handle are cleaned up the asset is cleaned up.
     */
    let mesh = meshes.add(PADDLE_SHAPE);
    let material = materials.add(PADDLE_COLOR);
    let half_window_size = window.resolution.size() / 2.;
    let padding = 30.;

    let human_player_position = Vec2::new(-half_window_size.x + padding, 0.);

    commands.spawn((
        HumanPlayer,
        Paddle,
        Mesh2d(mesh.clone()),
        MeshMaterial2d(material.clone()),
        Position(human_player_position),
        /*
         * we don't have to add the Collider component here,
         * because we added it by default when defining the Paddle struct
         * (see comparison with spawning a Wall object)
         */
    ));

    let ai_player_position = Vec2::new(half_window_size.x - padding, 0.);

    commands.spawn((
        AiPlayer,
        Paddle,
        Mesh2d(mesh.clone()),
        MeshMaterial2d(material.clone()),
        Position(ai_player_position),
        /*
         * we don't have to add the Collider component here,
         * because we added it by default when defining the Paddle struct
         * (see comparison with spawning a Wall object)
         */
    ));
}

pub fn handle_player_input_system(
    keyboard_input: Res<ButtonInput<KeyCode>>,
    /*
     * We are using "Single" for the querying the paddle controled by human player.
     * That's why we have to use "With<HumanPlayer>" as a filter.
     * If we used "With<Paddle>" as a filter instead, Bevy would find 2 paddles and because
     * we are using "Single" type, and not type "Query", the system function would not run
     * and our paddle would not move after we press ArrowUp or ArrowDown
     */
    mut paddle_velocity: Single<&mut Velocity, With<HumanPlayer>>,
) {
    /*
     * The keyboard_input.pressed will return true during a frame where the key-code we pass it
     * matches to a key pressed by a user.
     */
    if keyboard_input.pressed(KeyCode::ArrowUp) {
        paddle_velocity.0.y = PADDLE_SPEED;
    } else if keyboard_input.pressed(KeyCode::ArrowDown) {
        paddle_velocity.0.y = -PADDLE_SPEED;
    } else {
        paddle_velocity.0.y = 0.;
    }
}

pub fn move_ai_paddle(
    ai_paddle: Single<(&mut Velocity, &Position), With<AiPlayer>>,
    ball: Single<&Position, With<Ball>>,
) {
    let (mut velocity, position) = ai_paddle.into_inner();
    /*
     * Subtracting two vectors that represent coordinates in our game will give us a new vector pointing
     * from one to the other.
     * We can then use this new vector's y component to set our desired movement.
     */
    let a_to_b = ball.0 - position.0;
    velocity.0.y = a_to_b.y.signum() * PADDLE_SPEED;
}

pub fn move_paddles_system(mut paddles: Query<(&mut Position, &Velocity), With<Paddle>>) {
    for (mut position, velocity) in &mut paddles {
        position.0 += velocity.0;
    }
}

/*
 * Checks if paddles collide with any of the walls.
 * Force paddles' position inside the bounds when they do.
 */
pub fn constrain_paddle_position_system(
    mut paddles: Query<(&mut Position, &Collider), (With<Paddle>, Without<Wall>)>,
    walls: Query<(&mut Position, &Collider), (With<Wall>, Without<Paddle>)>,
) {
    for (mut paddle_position, paddle_collider) in &mut paddles {
        for (wall_position, wall_collider) in &walls {
            let paddle_bounding_box = Aabb2d::new(paddle_position.0, paddle_collider.half_size());
            let wall_bounding_box = Aabb2d::new(wall_position.0, wall_collider.half_size());

            /*
             * We are reusing the logic from "collide_with_side" function to determine which way
             * we need to push the paddle (either up or down) to keep it from going outside of the walls.
             */
            if let Some(collision) = collide_with_wall_side(paddle_bounding_box, wall_bounding_box)
            {
                match collision {
                    // we hit the top side of the wall -> we hit the wall which is down
                    Collision::Top => {
                        paddle_position.0.y = wall_position.0.y
                            + wall_collider.half_size().y
                            + paddle_collider.half_size().y;
                    }
                    // we hit the bottom side of the wall -> we hit the wall which is up
                    Collision::Bottom => {
                        paddle_position.0.y = wall_position.0.y
                            - wall_collider.half_size().y
                            - paddle_collider.half_size().y;
                    }
                    _ => {}
                }
            }
        }
    }
}
