use bevy::{
    ecs::{
        entity::Entity,
        event::EntityEvent,
        observer::On,
        query::{With, Without},
        system::{Commands, Query, ResMut, Single},
    },
    log::info,
    window::Window,
};

use crate::{
    ball::components::Ball,
    collision::Collider,
    components::{AiPlayer, HumanPlayer, Position},
    score::resources::Score,
};

/*
 * In Bevy, there are two ways to communicate between our systems:
 *      "Messages" - for publish/subscribe style communication within a couple frames
 *      "Events" - for immediately triggering other systems this frame
 *
 *
 * Here we are using events which will immediately trigger both our systems when someone scores.
 *
 * There are two kinds of events:
 *      "Event" - for global events
 *      "EntityEvent" - for events relating to a specific entity
 *
 * Here we are making an EntityEvent which expects a struct that contains at least an entity field.
 * You can rename this by setting the "#[event_target]" on the field that holds an Entity.
 */
#[derive(EntityEvent)]
pub struct Scored {
    #[event_target]
    pub scorer: Entity,
}

/*
 * A system which detects a goal and fires the "Scored" event.
 */
pub fn detect_goal_system(
    mut commands: Commands,
    window: Single<&Window>,
    ball: Single<(&Position, &Collider), With<Ball>>,
    human_player: Single<Entity, (With<HumanPlayer>, Without<AiPlayer>)>,
    ai_player: Single<Entity, (With<AiPlayer>, Without<HumanPlayer>)>,
) {
    let (ball_position, ball_collider) = ball.into_inner();
    let half_window_size = window.resolution.size() / 2.;

    if ball_position.0.x - ball_collider.half_size().x > half_window_size.x {
        /*
         * We can use both here:
         *      Scored { scorer: human_player.into_inner() }
         *      Scored { scorer: *human_player }
         */
        commands.trigger(Scored {
            scorer: human_player.into_inner(),
        });
    }

    if ball_position.0.x + ball_collider.half_size().x < half_window_size.x {
        /*
         * We can use both here:
         *      Scored { scorer: *ai_player }
         *      Scored { scorer: ai_player.into_inner() }
         */
        commands.trigger(Scored { scorer: *ai_player });
    }
}

/*
 * This system is special because of its first system parameter: "On".
 * This makes it observer which is a callback that responds to certain events.
 */
pub fn update_score_system(
    event: On<Scored>,
    mut score: ResMut<Score>,
    is_human_player: Query<&HumanPlayer>,
    is_ai_player: Query<&AiPlayer>,
) {
    if is_ai_player.get(event.scorer).is_ok() {
        score.ai_player += 1;
        info!("AI scored! {} - {}", score.human_player, score.ai_player);
    }

    if is_human_player.get(event.scorer).is_ok() {
        score.human_player += 1;
        info!(
            "Human player scored! {} - {}",
            score.human_player, score.ai_player
        );
    }
}
