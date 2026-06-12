use bevy::color::Color;

pub const WINDOW_RESOLUTION: (u32, u32) = (1400, 900);
pub const BACKGROUND_COLOR: Color = Color::srgb(13. / 255.0, 13. / 255., 24. / 255.);
pub const CANVAS_COLOR: Color = Color::srgb(31. / 255.0, 31. / 255., 45. / 255.);
pub const DEFAULT_TEXT_COLOR: Color = Color::srgb(200. / 255.0, 200. / 255., 200. / 255.);

pub const INSTRUCTIONS_FONT_SIZE: f32 = 24.;

pub const GRID_SIZE: u32 = 20;
pub const CELL_PIXELS: u32 = 30; // number of pixels for each cell
