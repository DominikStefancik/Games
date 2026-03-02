use bevy::{
    asset::Assets,
    ecs::system::{Commands, ResMut, Single},
    math::{Vec2, primitives::Rectangle},
    mesh::{Mesh, Mesh2d},
    sprite_render::{ColorMaterial, MeshMaterial2d},
    window::Window,
};

use crate::{
    collision::Collider,
    components::Position,
    wall::components::{WALL_COLOR, WALL_HEIGHT, Wall},
};

pub fn spawn_walls_system(
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
    let material = materials.add(WALL_COLOR);
    let padding = 20.;

    let Window { resolution, .. } = window.into_inner();
    let border_shape = Rectangle::new(resolution.width(), WALL_HEIGHT);
    let mesh = meshes.add(border_shape);

    let top_position = Vec2::new(0., resolution.height() / 2. - padding);

    commands.spawn((
        Wall,
        Mesh2d(mesh.clone()),
        MeshMaterial2d(material.clone()),
        Position(top_position),
        /*
         * we have to add the Collider component here,
         * because we didn't add it by default when defining the Wall struct
         * (see comparison with spawning a Paddle object)
         */
        Collider(border_shape),
    ));

    let bottom_position = Vec2::new(0., -resolution.height() / 2. + padding);

    commands.spawn((
        Wall,
        Mesh2d(mesh.clone()),
        MeshMaterial2d(material.clone()),
        Position(bottom_position),
        /*
         * we have to add the Collider component here,
         * because we didn't add it by default when defining the Wall struct
         * (see comparison with spawning a Paddle object)
         */
        Collider(border_shape),
    ));
}
