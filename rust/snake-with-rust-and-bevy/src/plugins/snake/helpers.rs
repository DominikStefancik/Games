use bevy::{ecs::system::Commands, math::Vec2, sprite::Sprite, transform::components::Transform};

use crate::plugins::{
    shared::{CELL_PADDING, Grid, SNAKE_BODY_COLOR, SNAKE_HEAD_COLOR},
    snake::{Snake, components::SnakeSegmentSprite},
};

pub fn render_snake(commands: &mut Commands, grid: &Grid, snake: &Snake) {
    for (index, &segment) in snake.segments.iter().enumerate() {
        let color = if index == 0 {
            SNAKE_HEAD_COLOR
        } else {
            SNAKE_BODY_COLOR
        };
        commands.spawn((
            Sprite::from_color(color, Vec2::splat((grid.pixels - CELL_PADDING) as f32)),
            Transform::from_translation(grid.to_pixels(segment, 1.)),
            SnakeSegmentSprite,
        ));
    }
}
