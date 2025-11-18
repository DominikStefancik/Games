use bevy::ecs::component::Component;

// Represents score for the human player shown on the screen
#[derive(Component)]
pub struct HumanPlayerScoreUi;

// Represents score for the ai player shown on the screen
#[derive(Component)]
pub struct AiPlayerScoreUi;
