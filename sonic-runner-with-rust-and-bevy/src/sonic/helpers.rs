use std::time::Duration;

use bevy::ecs::{entity::Entity, system::Commands};

use crate::{
    entities::components::{Animation, AnimationTimer},
    sonic::components::{
        SONIC_JUMP_ANIMATION_DURATION, SONIC_RUN_ANIMATION_DURATION, SonicAnimationKind,
    },
};

pub fn switch_sonic_animation(
    kind: SonicAnimationKind,
    commands: &mut Commands,
    entity: Entity,
    animation_timer: &mut AnimationTimer,
) {
    match kind {
        SonicAnimationKind::Run => {
            let run_animation = Animation::new(0, 7);
            commands.entity(entity).insert(run_animation);
            animation_timer
                .0
                .set_duration(Duration::from_secs_f32(SONIC_RUN_ANIMATION_DURATION));
        }
        SonicAnimationKind::Jump => {
            let jump_animation = Animation::new(8, 15);
            commands.entity(entity).insert(jump_animation);
            animation_timer
                .0
                .set_duration(Duration::from_secs_f32(SONIC_JUMP_ANIMATION_DURATION));
        }
    }
}
