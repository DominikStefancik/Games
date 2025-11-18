use bevy::{
    asset::Assets,
    ecs::{
        query::With,
        system::{Commands, ResMut, Single},
    },
    mesh::{Mesh, Mesh2d},
    sprite_render::{ColorMaterial, MeshMaterial2d},
};

use crate::components::Position;
use crate::{
    ball::components::{BALL_COLOR, BALL_SHAPE, BALL_SPEED, Ball},
    components::Velocity,
};

/*
 * To render a shape onto the screen we need two things:
 *      Mesh: the transparent shape of our object
 *      Material: the texture we should paint onto the shape
 *
 * For defining our shape we use a Mesh2d that will store all the vertices (points in space) that make up
 * the shape we want.
 *
 * For the texture that gets put onto our shape we will need a MeshMaterial2d that we give a Color::srgb
 * which will tell Bevy's renderer to paint our shape one solid color.
 */
pub fn spawn_ball_system(
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
    let mesh = meshes.add(BALL_SHAPE);
    let material = materials.add(BALL_COLOR);

    /*
     * Because our Ball requires Position and Position requires Transform, spawning a single Ball component gives us
     * Ball, Position and Transform
     */
    commands.spawn((Ball, Mesh2d(mesh), MeshMaterial2d(material)));
}

/*
 * We have a query that uses both generic arguments: Query<D, F>
 *      The first one D is what we want returned. So we are asking for all the Position components.
 *      The second F is a filter which is modifying our request to only get Position components
 *      from entities which also have a Ball.
 *
 * The upside of using the filter is that the Ball is not actually returned from the query. It is only changing
 * which Position components get returned to us.
 *
 * Note:
 * "Single" is special version of a Query that will skip the system if none or more than one match of the query exists.
 */
pub fn move_ball_system(ball: Single<(&mut Position, &Velocity), With<Ball>>) {
    let (mut position, velocity) = ball.into_inner();
    position.0 += velocity.0 * BALL_SPEED;
}
