// Sets up default plugins like window, assets, inpupts, etc.

use bevy::{
    DefaultPlugins,
    app::{App, PluginGroup},
    camera::ClearColor,
    color::Color,
    window::{Window, WindowPlugin, WindowResolution},
};
use std::num::NonZero;

const WINDOW_RESOLUTION: (u32, u32) = (1000, 800);
const BACKGROUND_COLOR: Color = Color::srgb(0.0, 0.0, 0.0);

pub fn plugin(app: &mut App) {
    let primary_window = Window {
        title: "Rust Pong".into(),
        resizable: false,
        resolution: WindowResolution::new(WINDOW_RESOLUTION.0, WINDOW_RESOLUTION.1),
        canvas: Some("#bevy".to_owned()),
        desired_maximum_frame_latency: NonZero::new(1u32),
        ..Default::default()
    };

    app.insert_resource(ClearColor(BACKGROUND_COLOR))
        .add_plugins(DefaultPlugins.set(WindowPlugin {
            primary_window: Some(primary_window),
            ..Default::default()
        }));
}
