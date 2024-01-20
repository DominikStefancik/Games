// By default, Bevy finds all assets in the "assets" folder
pub const PLAYER_SPRITE: &str = "player_a.png";
pub const PLAYER_SIZE: (f32, f32) = (144_f32, 75_f32);
pub const PLAYER_LASER_SPRITE: &str = "laser_a.png";
pub const PLAYER_LASER_SIZE: (f32, f32) = (9., 54.);
// defines a delay after the player will be again respawned
pub const PLAYER_RESPAWN_DELAY: f64 = 2.;

pub const ENEMY_SPRITE: &str = "enemy_a.png";
pub const ENEMY_SIZE: (f32, f32) = (144_f32, 75_f32);
pub const ENEMY_LASER_SPRITE: &str = "laser_b.png";
pub const ENEMY_LASER_SIZE: (f32, f32) = (17., 55.);

pub const ENEMY_FORMATION_MEMBERS_MAX: u8 = 2;

pub const EXPLOSION_SHEET: &str = "explosions_a_sheet.png";
pub const EXPLOSION_SHEET_CELL_SIZE: f32 = 64.;
pub const EXPLOSION_SHEET_SIZE: usize = 4;
pub const EXPLOSION_LENGTH: usize = 16;

pub const SPRITE_SCALE: f32 = 0.5;

pub const TIME_STEP: f32 = 2.0;
pub const BASE_SPEED: f32 = 2.0;
