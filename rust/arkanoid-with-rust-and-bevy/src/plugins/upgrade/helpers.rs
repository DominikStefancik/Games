use rand::RngExt;

use crate::plugins::{BrickType, Randomizer};

pub fn should_spawn_upgrade(brick_type: BrickType, randomizer: &mut Randomizer) -> bool {
    let percentage = match brick_type {
        BrickType::Grey => 0.075,
        BrickType::Bronze => 0.1,
        BrickType::Purple => 0.15,
        BrickType::Orange => 0.2,
        BrickType::Red => 0.25,
        BrickType::Green => 0.3,
        BrickType::Blue => 0.5,
    };

    let random_number = randomizer.rng.random_range(0_f32..1_f32);

    random_number <= percentage
}
