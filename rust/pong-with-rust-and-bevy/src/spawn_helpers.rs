use bevy::{camera::Camera2d, ecs::system::Commands};

pub fn spawn_empty_entity(commands: &mut Commands) {
    /*
     * An Entity is really an ID. Kind of like a pointer we can use to find the components that are associated to it.
     * Bevy is storing all our components in big arrays of the same type, and this entity is the index in each array
     * that makes up that entity's data.
     *
     * The method "spawn_empty" on "Commands" will create a new Entity.
     * If this were a traditional database backed application, you can think of adding an entity just like adding
     * a new row.
     *
     * Entities themselves are not the things being renderedon the screen. Instead the components of an entity
     * are what determine if Bevy draws them on the screen at all.
     */
    commands.spawn_empty();
}

pub fn spawn_camera(commands: &mut Commands) {
    /*
     * Inserting into an entity just means to associate the components to an Entity by placing it inside the array of
     * other components at an index that matches that entity's index.
     * Components are stored in big arrays of the same type for performance reasons. We essentially added a new column
     * and associated it to our row (the entity).
     *
     * The Camera2d component will also add any of the other required components it needs onto your entity if you have
     * not added them yourself.
     */
    commands.spawn_empty().insert(Camera2d);

    /*
     * Spawning entities and components together is so common that there is a much more convenient spawn method you
     * can use to say the same thing:
     *      commands.spawn(Camera2d);
     *
     * For spawning many components at once on a new entity, we can give spawn a tuple
     */
}
