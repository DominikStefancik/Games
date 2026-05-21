use bevy::{
    color::Color,
    ecs::{
        change_detection::DetectChanges,
        children,
        entity::Entity,
        event::EntityEvent,
        observer::On,
        query::{With, Without},
        system::{Commands, Query, Res, ResMut, Single},
    },
    log::info,
    text::{Justify, TextColor, TextFont, TextLayout},
    ui::{JustifyContent, Node, PositionType, percent, px, widget::Text},
    window::Window,
};

use crate::{
    ball::components::Ball,
    collision::Collider,
    components::{AiPlayer, HumanPlayer, Position},
    score::{
        components::{AiPlayerScoreUi, HumanPlayerScoreUi},
        resources::Score,
    },
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

    if ball_position.0.x + ball_collider.half_size().x < -half_window_size.x {
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

pub fn spawn_scoreboard_system(mut commands: Commands) {
    // Create a container that will center everything
    let container = Node {
        width: percent(100.),
        height: percent(100.),
        justify_content: JustifyContent::Center,
        ..Default::default()
    };

    // Then add a container for the text
    let header = Node {
        width: px(200.),
        height: px(100.),
        ..Default::default()
    };

    // The human player's score on the left hand side
    let human_player_score = (
        HumanPlayerScoreUi,
        Text::new("0"),
        TextFont::from_font_size(72.),
        TextColor(Color::WHITE),
        TextLayout::new_with_justify(Justify::Center),
        Node {
            position_type: PositionType::Absolute,
            top: px(30.),
            left: px(-50.),
            ..Default::default()
        },
    );

    // The human player's score on the left hand side
    let ai_player_score = (
        AiPlayerScoreUi,
        Text::new("0"),
        TextFont::from_font_size(72.),
        TextColor(Color::WHITE),
        TextLayout::new_with_justify(Justify::Center),
        Node {
            position_type: PositionType::Absolute,
            top: px(30.),
            right: px(-50.),
            ..Default::default()
        },
    );

    /*
     * The children! macro creates a relationship in Bevy. In this case we are using the builtin Children/ChildOf
     * relationship. This lets an entity have many Children and each child contains a ChildOf(Entity) pointing to
     * the parent.
     *
     * Bevy keeps the Children in sync with each of the ChildOf components so we can easily access them from either
     * direction.
     *
     * If something is a ChildOf another entity, it will keep its Transform in sync and relative to that parent.
     * This is how these Node components can be placed relatively to one another.
     */
    commands.spawn((
        container,
        children![(header, children![human_player_score, ai_player_score])],
    ));
}

pub fn update_scoreboard_system(
    score: Res<Score>,
    mut human_player_score: Single<&mut Text, (With<HumanPlayerScoreUi>, Without<AiPlayerScoreUi>)>,
    mut ai_player_score: Single<&mut Text, (With<AiPlayerScoreUi>, Without<HumanPlayerScoreUi>)>,
) {
    /*
     * Here we are using the Score resource we created and ask if it "is_changed()" which uses Bevy's change detection
     * features to only run our logic on frames where the scores value has changed.
     */
    if score.is_changed() {
        human_player_score.0 = score.human_player.to_string();
        ai_player_score.0 = score.ai_player.to_string();
    }
}
