use bevy::ecs::resource::Resource;

#[derive(Resource)]
pub struct GameSettings {
    pub speed: f32,
    pub score: u32,
    pub score_multiplier: u8,
    pub best_score: u32,
}

const INITIAL_SPEED: f32 = 10.;

impl GameSettings {
    pub fn new() -> Self {
        GameSettings {
            speed: INITIAL_SPEED,
            score: 0,
            score_multiplier: 0,
            best_score: 0,
        }
    }

    pub fn increase_speed(self: &mut Self, speed_increment: f32) {
        self.speed += speed_increment;
    }

    pub fn increase_score_multiplier(self: &mut Self) {
        self.score_multiplier += 1;
    }

    pub fn reset_score_multiplier(self: &mut Self) {
        self.score_multiplier = 0;
    }

    pub fn reset(self: &mut Self) {
        self.speed = INITIAL_SPEED;
        self.score = 0;
        self.score_multiplier = 0;
    }
}
