use std::time::Duration;

use bevy::time::TimeUpdateStrategy;
use snake_with_rust_and_bevy::plugins::food::FoodConsumed;

use crate::support::{TestApp, get_food_position};

mod support;

#[test]
fn new_food_appears_at_different_place_after_previous_one_is_consumed() {
    let mut test_app = TestApp::new();

    /*
     * Calling test_app.update() in a loop doesn't advance game time by goven amount of milliseconds per call;
     * It advances it by however much real wall-clock time elapsed between your two update() calls,
     * which for back-to-back function calls in a test is typically microseconds. So Time::delta() is essentially zero,
     * and anything driven by elapsed time (a movement timer, a "move every N ms" check, etc.) barely progresses.
     *
     * Bevy has a resource built specifically for this - TimeUpdateStrategy - deterministic, manually-controlled
     * time advancement in tests.
     * Time will be incremented by the specified Duration each frame — For most cases,
     * TimeUpdateStrategy::Automatic is fine. When writing tests, dealing with networking or similar,
     * you may prefer to set the next Time value manually.
     *
     * Once this is set, every app.update() call advances Time by exactly the duration you specified,
     * regardless of how fast your test actually executes.
     */
    test_app
        .app
        .insert_resource(TimeUpdateStrategy::ManualDuration(Duration::from_millis(
            200,
        )));
    // Trigger all the Startup systems; first 200ms tick also happens here
    test_app.update();

    let initial_food_position = {
        let world = test_app.app.world_mut();
        get_food_position(world)
    };

    let world = test_app.app.world_mut();
    world.trigger(FoodConsumed);
    // advances another 200ms, snake should move now
    test_app.update();

    let new_food_position = {
        let world = test_app.app.world_mut();
        get_food_position(world)
    };

    assert_ne!(
        new_food_position.column, initial_food_position.column,
        "New food should be at a different position"
    );
}
