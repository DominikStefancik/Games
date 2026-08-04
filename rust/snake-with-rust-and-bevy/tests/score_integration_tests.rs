use std::time::Duration;

use bevy::{state::state::NextState, time::TimeUpdateStrategy};
use snake_with_rust_and_bevy::plugins::{food::FoodConsumed, game::GameState};

use crate::support::{TestApp, get_score};

mod support;

#[test]
fn current_score_is_updated_after_food_is_consumed() {
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

    let initial_score = {
        let world = test_app.app.world_mut();
        get_score(world).current
    };

    let world = test_app.app.world_mut();
    world.trigger(FoodConsumed);
    // advances another 200ms, snake should move now
    test_app.update();

    let updated_score = {
        let world = test_app.app.world_mut();
        get_score(world).current
    };

    assert_ne!(
        initial_score, updated_score,
        "Updated score should be different"
    );
    assert_eq!(
        updated_score,
        initial_score + 1,
        "Updated score should be bigger with 1"
    );
}

#[test]
fn best_score_is_updated_after_game_is_over() {
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

    let initial_score = {
        let world = test_app.app.world_mut();
        get_score(world)
    };

    let world = test_app.app.world_mut();
    world.trigger(FoodConsumed);
    // advances another 200ms, snake should move now
    test_app.update();

    let updated_score = {
        let world = test_app.app.world_mut();
        get_score(world)
    };

    assert_eq!(
        updated_score.current,
        initial_score.current + 1,
        "Updated score should be bigger with 1"
    );
    assert_eq!(
        updated_score.best, initial_score.best,
        "Best score should not be updated"
    );
    assert_eq!(
        updated_score.best,
        updated_score.current - 1,
        "Best score should be smaller then current one with 1"
    );

    let world = test_app.app.world_mut();
    world
        .get_resource_mut::<NextState<GameState>>()
        .expect("Game State should be inserted")
        .set(GameState::GameOver);
    // advances another 200ms, snake should move now
    test_app.update();

    let updated_score = {
        let world = test_app.app.world_mut();
        get_score(world)
    };

    assert_ne!(
        updated_score.best, initial_score.best,
        "Best score should be updated"
    );
    assert_eq!(
        updated_score.best, updated_score.current,
        "Best score should be the same as current"
    );
}
