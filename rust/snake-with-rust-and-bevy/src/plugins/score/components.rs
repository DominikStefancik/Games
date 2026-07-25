use bevy::{ecs::component::Component, time::Timer};

#[derive(Component)]
pub struct ScoreLabelUi;

#[derive(Component)]
pub struct ScoreTextUi;

#[derive(Component)]
pub struct BestScoreLabelUi;

#[derive(Component)]
pub struct BestScoreTextUi;

#[derive(Component, Debug)]
pub struct ScorePop(pub Timer);
