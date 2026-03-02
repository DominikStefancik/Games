use bevy::ecs::resource::Resource;

/*
 * "Resource" has a great use in situations where you only want one piece of data to exist and it does not make sense
 * to put on any single entity.
 *
 * A Resource is just a component without an entity.
 * They are singleton components we can easily access from our systems.
 */
#[derive(Resource)]
pub struct Score {
    pub human_player: u16,
    pub ai_player: u16,
}
