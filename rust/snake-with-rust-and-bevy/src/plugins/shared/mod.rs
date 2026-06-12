use bevy::app::{App, Plugin, Startup};

use crate::core::{GridSize, load_fonts};

pub struct SharedPlugin;

impl Plugin for SharedPlugin {
    fn build(&self, app: &mut App) {
        app.insert_resource(GridSize::default())
            .add_systems(Startup, load_fonts);
    }
}
