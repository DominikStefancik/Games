use crate::components::{BackgroundMusic, Ball, Player, ScoreBoard, Side};
use crate::constants::{
    ARENA_HEIGHT, ARENA_WIDTH, GRAVITY_ACCELERATION, PLAYER_HEIGHT, PLAYER_SPEED, PLAYER_WIDTH,
};
use crate::helpers::spawn_sound;
use crate::resources::Score;
use bevy::prelude::{
    AudioSink, AudioSinkPlayback, ButtonInput, Commands, Entity, KeyCode, Query, Res, ResMut,
    TextUiWriter, Time, Transform, With,
};
use rand::Rng;

/*
 * Generally, all Bevy system functions work in this way; various arguments to retrieve resources,
 * entities, components, and other features can be directly added to the function interface,
 * and Bevy will connect the code automatically internally (i.e. it will pass the values for these
 * arguments).
 */

pub fn move_player_system(
    keyboard_input: Res<ButtonInput<KeyCode>>,
    /*
     * Provides a reference to the time resource. Since our player system function can be called
     * with different amounts of time between steps, we’ll use this resource to determine the time
     * since last step, which will help us ensure player movement is smooth.
     */
    time: Res<Time>,
    // a query providing each entity that contains both a Player and a Transform
    mut query: Query<(&Player, &mut Transform)>,
) {
    for (player, mut transform) in query.iter_mut() {
        let direction = if keyboard_input.pressed(player.side.move_cat_left_key()) {
            -1.0_f32
        } else if keyboard_input.pressed(player.side.move_cat_right_key()) {
            1.0_f32
        } else {
            0.0_f32
        };

        let offset = direction * PLAYER_SPEED * time.delta_secs();

        // apply movement deltas
        transform.translation.x += offset;

        // we need to make sure that the cats don't moe outside the window
        // and to the opponent's area
        let (left_limit, right_limit) = player.side.cat_movement_range();
        transform.translation.x = transform.translation.x.clamp(left_limit, right_limit);
    }
}

pub fn move_ball_system(time: Res<Time>, mut query: Query<(&mut Ball, &mut Transform)>) {
    for (mut ball, mut transform) in query.iter_mut() {
        // Apply movement deltas
        // For the accurate simulation of a falling ball we use
        // algorithm called Velocity Verlet integration
        transform.translation.x += ball.velocity.x * time.delta_secs();
        transform.translation.y +=
            (ball.velocity.y + time.delta_secs() * GRAVITY_ACCELERATION / 2.) * time.delta_secs();
        ball.velocity.y += time.delta_secs() * GRAVITY_ACCELERATION;
    }
}

fn is_point_in_rectangle(
    ball_x: f32,
    ball_y: f32,
    player_box_boundary_left: f32,
    player_box_boundary_bottom: f32,
    player_box_boundary_right: f32,
    player_box_boundary_top: f32,
) -> bool {
    ball_x >= player_box_boundary_left
        && ball_x <= player_box_boundary_right
        && ball_y >= player_box_boundary_bottom
        && ball_y <= player_box_boundary_top
}

pub fn bounce_ball_system(
    mut commands: Commands,
    mut ball_query: Query<(&mut Ball, &Transform)>,
    player_query: Query<(&Player, &Transform)>,
) {
    for (mut ball, ball_transform) in ball_query.iter_mut() {
        let ball_x = ball_transform.translation.x;
        let ball_y = ball_transform.translation.y;

        if ball_y <= ball.radius && ball.velocity.y < 0. {
            spawn_sound(&mut commands, ball.bounce_sound.clone());
            ball.velocity.y *= -1.;
        } else if ball_y >= ARENA_HEIGHT - ball.radius && ball.velocity.y > 0. {
            spawn_sound(&mut commands, ball.bounce_sound.clone());
            ball.velocity.y *= -1.;
        } else if ball_x <= ball.radius && ball.velocity.x < 0. {
            spawn_sound(&mut commands, ball.bounce_sound.clone());
            ball.velocity.x *= -1.;
        } else if ball_x >= ARENA_WIDTH - ball.radius && ball.velocity.x > 0. {
            spawn_sound(&mut commands, ball.bounce_sound.clone());
            ball.velocity.x *= -1.;
        }

        for (player, player_transform) in player_query.iter() {
            let player_x = player_transform.translation.x;
            let player_y = player_transform.translation.y;

            if is_point_in_rectangle(
                ball_x,
                ball_y,
                player_x - PLAYER_WIDTH / 2.0 - ball.radius,
                player_y - PLAYER_HEIGHT / 2.0 - ball.radius,
                player_x + PLAYER_WIDTH / 2.0 + ball.radius,
                player_y + PLAYER_HEIGHT / 2.0 + ball.radius,
            ) && ball.velocity.y < 0.
            {
                spawn_sound(&mut commands, ball.bounce_sound.clone());
                // Only bounce when a ball is falling
                ball.velocity.y *= -1.;

                let mut rng = rand::rng();
                /*
                 * To give the game some playability, we randomly speed up or slow down
                 * the ball in the x-axis on collision,so the ball’s trajectory is unpredictable
                 */
                match player.side {
                    Side::Left => {
                        ball.velocity.x = ball.velocity.x.abs() * rng.random_range(0.6..1.4)
                    }
                    Side::Right => {
                        ball.velocity.x = -1. * ball.velocity.x.abs() * rng.random_range(0.6..1.4)
                    }
                }
            }
        }
    }
}

pub fn update_score_system(
    mut commands: Commands,
    mut score: ResMut<Score>,
    mut ball_query: Query<(&mut Ball, &mut Transform)>,
    score_board_query: Query<(&ScoreBoard, Entity)>,
    mut writer: TextUiWriter,
) {
    for (mut ball, mut transform) in ball_query.iter_mut() {
        let ball_x = transform.translation.x;
        let ball_y = transform.translation.y;

        if ball_y < ball.radius {
            spawn_sound(&mut commands, ball.score_sound.clone());
            if ball_x <= ARENA_WIDTH / 2. {
                score.right += 1;
                // change direction of the ball toward the right player
                ball.velocity.x = ball.velocity.x.abs();
            } else {
                score.left += 1;
                // change direction of the ball toward the left player
                ball.velocity.x = -ball.velocity.x.abs();
            }

            transform.translation.x = ARENA_WIDTH / 2.;
            transform.translation.y = ARENA_HEIGHT / 2.;
            ball.velocity.y = 0.; // reset to free drop

            // update score board
            for (score_board, entity) in score_board_query.iter() {
                *writer.text(entity, 0) = match score_board.side {
                    Side::Left => score.left.to_string(),
                    Side::Right => score.right.to_string(),
                }
            }
        }
    }
}

pub fn pause_background_music_system(
    keyboard_input: Res<ButtonInput<KeyCode>>,
    music_query: Query<&AudioSink, With<BackgroundMusic>>,
) {
    if keyboard_input.just_pressed(KeyCode::Space) {
        if let Ok(sink) = music_query.single() {
            sink.toggle_playback();
        }
    }
}
