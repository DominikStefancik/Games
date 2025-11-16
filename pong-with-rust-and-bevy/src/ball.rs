use crate::components::Position;
use bevy::{
    asset::Assets,
    color::Color,
    ecs::{
        component::Component,
        system::{Commands, ResMut},
    },
    math::primitives::Circle,
    mesh::{Mesh, Mesh2d},
    sprite_render::{ColorMaterial, MeshMaterial2d},
};

const BALL_RADIUS: f32 = 10.;
const BALL_SHAPE: Circle = Circle::new(BALL_RADIUS);
const BALL_COLOR: Color = Color::srgb(1., 0., 0.);

/*
 * We need something to mark our entity is a ball, rather than a wall or a paddle.
 * For this component, it's enough to just have it on our entity. It doesn't need any data.
 * When you use a component in this way its called a "marker component".
 */
#[derive(Component)]
/*
 * By adding a require macro to our ball we are telling Bevy that any entity with a Ball should also be spawned
 * with a Position.
 * So long as our Position has a default trait implemented, it will add that default if we do not add our own.
 */
#[require(Position)]
pub struct Ball;

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
