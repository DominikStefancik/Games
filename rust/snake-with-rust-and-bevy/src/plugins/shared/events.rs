use bevy::ecs::event::Event;

/*
 * An Event is something that “happens” at a given moment.
 *
 * To make an Event “happen”, you “trigger” it on a World using World::trigger or via a Command using Commands::trigger.
 * This causes any Observer watching for that Event to run immediately, as part of the World::trigger call.
 *
 * Note: If you need an Event to "carry" certain data, use EntityEvent
 */
#[derive(Event)]
pub struct GameStartTriggered;

#[derive(Event)]
pub struct GameRestarted;

#[derive(Event)]
pub struct FoodConsumed;

#[derive(Event)]
pub struct SnakeDied;
