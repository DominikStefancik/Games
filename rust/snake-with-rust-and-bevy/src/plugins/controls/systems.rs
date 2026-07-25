use bevy::{
    ecs::system::{Res, ResMut},
    input::{ButtonInput, keyboard::KeyCode},
};

use crate::{
    core::{Direction, DirectionQueue},
    plugins::snake::Snake,
};

pub fn enqueue_snake_direction_on_keypress(
    input: Res<ButtonInput<KeyCode>>,
    mut queue: ResMut<DirectionQueue>,
    snake: Res<Snake>,
) {
    let arrow_keys = [
        KeyCode::ArrowLeft,
        KeyCode::ArrowRight,
        KeyCode::ArrowUp,
        KeyCode::ArrowDown,
    ];

    for key in arrow_keys.iter().filter(|key| input.just_pressed(**key)) {
        if let Some(direction) = Direction::from_key(key)
            && !snake.direction.is_opposite(&direction)
        {
            queue.0.push_back(direction);
        };
    }
}
