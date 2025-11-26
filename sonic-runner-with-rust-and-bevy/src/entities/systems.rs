use bevy::{
    ecs::system::{Query, Res},
    sprite::Sprite,
    state::state::State,
    time::Time,
};

use crate::{
    entities::components::{Animation, AnimationTimer},
    game::GameState,
};

pub fn run_animations(
    time: Res<Time>,
    mut query: Query<(&Animation, &mut AnimationTimer, &mut Sprite)>,
    game_state: Res<State<GameState>>,
) {
    if *game_state.get() == GameState::Running {
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
}
