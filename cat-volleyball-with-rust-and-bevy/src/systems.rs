use crate::components::Player;
use crate::constants::PLAYER_SPEED;
use bevy::prelude::{Input, KeyCode, Query, Res, Time, Transform};

/*
 * Generally, all Bevy system functions work in this way; various arguments to retrieve resources,
 * entities, components, and other features can be directly added to the function interface,
 * and Bevy will connect the code automatically internally (i.e. it will pass the values for these
 * arguments).
 */

pub fn move_player_system(
    keyboard_input: Res<Input<KeyCode>>,
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

        let offset = direction * PLAYER_SPEED * time.delta_seconds();

        // apply movement deltas
        transform.translation.x += offset;

        // we need to make sure that the cats don't moe outside of the window
        // and to the opponent's area
        let (left_limit, right_limit) = player.side.cat_movement_range();
        transform.translation.x = transform.translation.x.clamp(left_limit, right_limit);
    }
}
