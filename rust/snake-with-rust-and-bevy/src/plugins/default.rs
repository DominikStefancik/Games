use std::num::NonZero;

use bevy::{
    DefaultPlugins,
    app::{App, PluginGroup},
    window::{Window, WindowPlugin, WindowResolution},
};

use crate::core::WINDOW_RESOLUTION;

pub fn default_plugin(app: &mut App) {
    let primary_window = Window {
        title: "Snake".into(),
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
