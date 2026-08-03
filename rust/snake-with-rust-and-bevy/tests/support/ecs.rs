use std::sync::LazyLock;

use bevy::{
    MinimalPlugins,
    app::App,
    asset::AssetPlugin,
    audio::AudioPlugin,
    ecs::world::World,
    state::app::StatesPlugin,
    text::TextPlugin,
    time::{Fixed, Time},
};
use snake_with_rust_and_bevy::plugins::{
    FoodPlugin, GamePlugin, SharedPlugin, SnakePlugin, shared::GridPosition, snake::Snake,
};

static TEST_ENV_VARIABLES: LazyLock<()> = LazyLock::new(|| unsafe {
    /*
     * Safety: Called once during the test setup before any other threads spawn.
     * We only mutate the process environment when the variables have not been set by the caller,
     * preserving explicit user overrides.
     */

    /*
     * The following 3 settings are recommended by Bevy to run a headless app for tests.
     */
    if std::env::var("WGPU_BACKEND").is_err() {
        // By setting the environment variable "WGPU_BACKEND" to null, test cases can be run without a need for GPUs
        // This is useful if the test cases need to be run on Github withot neeeding the GPU
        std::env::set_var("WGPU_BACKEND", "null");
    }

    if std::env::var("WGPU_POWER_PREF").is_err() {
        // We are setting this so the headless app for test will run on low power mode
        std::env::set_var("WGPU_POWER_PREF", "low_power");
    }

    if std::env::var("BEVY_LOG").is_err() {
        std::env::set_var("BEVY_LOG", "off");
    }
});

/// An utility wrapper around a headless Bevy "App" configured with the game plugins
pub struct TestApp {
    pub app: App,
}

impl TestApp {
    /// Create a new test application with minimal plugins and the game systems
    pub fn new() -> Self {
        // Lazily load environment variables
        LazyLock::force(&TEST_ENV_VARIABLES);
        let mut app = App::new();

        /*
         * Using "DefaultPlugins" in tests is generally overkill — and can actually be a problem — for integration tests,
         * particularly in CI. It'll fix immediate panics because it registers every built-in asset type
         * (Font, AudioSource, Image, etc.) via each subsystem's own plugin,
         * but it also pulls in things you almost certainly don't want in a test:
         *       - "WinitPlugin" tries to open a real OS window. On a headless CI runner (no display server).
         *           WinitPlugin will panic in environments without a display server.
         *       - "RenderPlugin" tries to initialize a real GPU backend via wgpu, which can be slow, flaky,
         *          or unavailable in CI too.
         *       - Audio, accessibility, diagnostics, etc. — all extra overhead/state we don't need for logic tests.
         *
         * Rather than reaching for "DefaultPlugins", it's usually better to stay on "MinimalPlugins" and add back only
         * the specific plugins that register the asset/resource types our game code actually touches
         */
        app.add_plugins(MinimalPlugins)
            .add_plugins(AssetPlugin {
                watch_for_changes_override: Some(false),
                ..Default::default()
            })
            .add_plugins(StatesPlugin)
            .add_plugins(AudioPlugin::default()) // registers AudioSource
            .add_plugins(TextPlugin);
        app.add_plugins((SharedPlugin, GamePlugin, SnakePlugin, FoodPlugin));

        if app.world().get_resource::<Time<Fixed>>().is_none() {
            app.world_mut().init_resource::<Time<Fixed>>();
        }

        Self { app }
    }

    /// Run the default "Update" schedule (also triggers one-off startup systems the first call).
    pub fn update(&mut self) {
        self.app.update();
    }
}

/// Helper function to get the snake head position (segment index 0) from the World
pub fn get_head_position(world: &mut World) -> GridPosition {
    let resource = world.get_resource::<Snake>();

    *resource
        .expect("Snake resource should be inserted")
        .segments
        .first()
        .expect("Snake should have head")
}
