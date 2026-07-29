use std::collections::VecDeque;

use bevy::{
    asset::{AssetServer, Handle},
    audio::AudioSource,
    ecs::{
        resource::Resource,
        world::{FromWorld, World},
    },
    math::{IVec2, Vec3},
    text::Font,
};
use rand::rngs::StdRng;

use crate::plugins::shared::{CELL_PIXELS, Direction, GRID_SIZE, GridPosition};

#[derive(Resource)]
pub struct GameFonts {
    pub bebas_neue_regular: Handle<Font>,
}

// When implementing this trait, we can then initialise a Resource on the App level
// by calling the ".init_resource::<GameFonts>()"
impl FromWorld for GameFonts {
    fn from_world(world: &mut World) -> Self {
        // in order to use the AssetServer, we have to add the DefaultPlugins as a first plugin,
        // because the AssetServer is registered there
        let asset_server = world.resource::<AssetServer>();

        let bebas_neue_regular = asset_server.load("fonts/BebasNeue-Regular.ttf");

        GameFonts { bebas_neue_regular }
    }
}

#[derive(Resource)]
pub struct GameSounds {
    pub eat: Handle<AudioSource>,
    pub die: Handle<AudioSource>,
}

/*
 * Here is a classic Snake bug: a player presses Right then Down very quickly within one tick.
 * If we change direction immediately, the snake goes right, then the same tick processes Down and the snake turns down.
 * But if the player pressed Left then Right, the snake reverses into itself and dies.
 * Creating a queue of directions fixes this. Each tick, we will pop one direction off the queue.
 */
#[derive(Resource)]
pub struct DirectionQueue(pub VecDeque<Direction>);

// If the data rarely changes during the game, it's better to use Resource rather than a Component
// From the perfomance point of view, Resources can render much faster then Components and can run in parallel
#[derive(Resource)]
pub struct Grid {
    pub size: IVec2,
    pub pixels: i32,
}

impl Grid {
    pub fn default() -> Self {
        Grid {
            size: IVec2::splat(GRID_SIZE),
            pixels: CELL_PIXELS,
        }
    }

    // translates grid position into a pixels position
    pub fn to_pixels(&self, position: GridPosition, z_index: f32) -> Vec3 {
        let half_width = self.size.x as f32 * self.pixels as f32 / 2.0;
        let half_height = self.size.y as f32 * self.pixels as f32 / 2.0;

        Vec3::new(
            position.column as f32 * self.pixels as f32 + self.pixels as f32 / 2.0 - half_width,
            position.row as f32 * self.pixels as f32 + self.pixels as f32 / 2.0 - half_height,
            z_index,
        )
    }
}

#[derive(Resource)]
pub struct Randomizer {
    pub rng: StdRng,
}
