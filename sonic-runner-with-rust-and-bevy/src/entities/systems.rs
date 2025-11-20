use bevy::{
    ecs::system::{Query, Res},
    sprite::Sprite,
    time::Time,
};

use crate::entities::components::{Animation, AnimationTimer};

pub fn run_animations(
    time: Res<Time>,
    mut query: Query<(&Animation, &mut AnimationTimer, &mut Sprite)>,
) {
    for (animation, mut timer, mut sprite) in &mut query {
        timer.tick(time.delta());

        if timer.just_finished()
            && let Some(atlas) = &mut sprite.texture_atlas
        {
            atlas.index = if atlas.index == animation.last_frame {
                animation.first_frame
            } else {
                atlas.index + 1
            }
        }
    }
}
