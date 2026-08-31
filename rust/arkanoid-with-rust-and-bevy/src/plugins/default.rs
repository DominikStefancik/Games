use std::num::NonZero;

use bevy::{
    DefaultPlugins,
    app::{App, PluginGroup},
    math::Vec2,
    window::{Window, WindowPlugin, WindowResolution},
};

pub const WINDOW_RESOLUTION: (u32, u32) = (1280, 720);
pub const WINDOW_RESOLUTION_HALF: Vec2 = Vec2::new(
    WINDOW_RESOLUTION.0 as f32 / 2.,
    WINDOW_RESOLUTION.1 as f32 / 2.,
);

pub fn default_plugin(app: &mut App) {
    let primary_window = Window {
        title: "Rust Arkanoid".into(),
        resizable: false,
        resolution: WindowResolution::new(WINDOW_RESOLUTION.0, WINDOW_RESOLUTION.1),
        canvas: Some("#bevy".to_owned()),
        desired_maximum_frame_latency: NonZero::new(1u32),
        ..Default::default()
    };

    app.add_plugins(DefaultPlugins.set(WindowPlugin {
        primary_window: Some(primary_window),
        ..Default::default()
    }));
}
