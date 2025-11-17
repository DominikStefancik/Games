use bevy::{
    asset::Assets,
    ecs::system::{Commands, ResMut, Single},
    math::Vec2,
    mesh::{Mesh, Mesh2d},
    sprite_render::{ColorMaterial, MeshMaterial2d},
    window::Window,
};

use crate::{
    components::{AiPlayer, HumanPlayer, Position},
    paddle::components::{PADDLE_COLOR, PADDLE_SHAPE, Paddle},
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
    ));

    let ai_player_position = Vec2::new(half_window_size.x - padding, 0.);

    commands.spawn((
        AiPlayer,
        Paddle,
        Mesh2d(mesh.clone()),
        MeshMaterial2d(material.clone()),
        Position(ai_player_position),
    ));
}
