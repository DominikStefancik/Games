use bevy::ecs::component::Component;

#[derive(Component)]
pub struct Heart {
    pub index: u16,
}

#[derive(Component)]
pub struct ScoreTextUi;
