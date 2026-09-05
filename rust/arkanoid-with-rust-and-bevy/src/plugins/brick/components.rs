use bevy::ecs::component::Component;

use crate::plugins::BrickType;

#[derive(Component)]
pub struct Brick {
    pub brick_type: BrickType,
}

impl Brick {
    pub fn update_type(&mut self) {
        let new_type = match self.brick_type {
            BrickType::Grey => BrickType::Bronze,
            BrickType::Bronze => BrickType::Purple,
            BrickType::Purple => BrickType::Orange,
            BrickType::Orange => BrickType::Red,
            BrickType::Red => BrickType::Green,
            BrickType::Green => BrickType::Blue,
            BrickType::Blue => BrickType::Blue,
        };

        self.brick_type = new_type;
    }
}
