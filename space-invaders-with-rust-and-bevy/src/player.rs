use crate::assets::{PLAYER_SIZE, SPRITE_SCALE};
use crate::components::{Player, Velocity};
use crate::resources::{GameTextures, WindowSize};
use bevy::prelude::{
    App, Commands, Input, KeyCode, Plugin, PostStartup, Query, Res, SpriteBundle, Transform,
    Update, Vec3, With,
};

// Use player functionality as a plugin
pub struct PlayerPlugin;

// Custom plugin in Bevy has to implement the trait "Plugin" in order to be able to be used
impl Plugin for PlayerPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(PostStartup, player_spawn_system)
            .add_systems(Update, player_movement_system)
            .add_systems(Update, player_keyboard_system);
    }
}

fn player_spawn_system(
    mut commands: Commands,
    game_textures: Res<GameTextures>,
    window_size: Res<WindowSize>,
) {
    // position the player at the bottom
    let bottom = -window_size.height / 2.;

    // Add the player
    commands
        .spawn(SpriteBundle {
            texture: game_textures.player.clone(),
            transform: Transform {
                translation: Vec3::new(
                    0_f32,
                    bottom + PLAYER_SIZE.1 / 2_f32 * SPRITE_SCALE + 5_f32,
                    10_f32,
                ),
                scale: Vec3::new(SPRITE_SCALE, SPRITE_SCALE, 1.),
                ..Default::default()
            },
            ..Default::default()
        })
        .insert(Player) // add custom component Player
        .insert(Velocity { x: 1., y: 0. }); // y-position will be the same for the player
}

// system which is changing position/movement of the player depending on the input velocity
// the first part of the Query says which we just want to read and which we want to mutate
// the second part (With<>) says that we want to apply read and write only on the Player component
fn player_movement_system(mut query: Query<(&Velocity, &mut Transform), With<Player>>) {
    for (velocity, mut transform) in query.iter_mut() {
        let translation = &mut transform.translation;
        translation.x += velocity.x;
        translation.y += velocity.y;
    }
}

// system which is changing the velocity of the player
fn player_keyboard_system(
    keyboard: Res<Input<KeyCode>>,
    // here the query only needs movement of a player which we are gonna change
    mut query: Query<&mut Velocity, With<Player>>,
) {
    // we know the query has only one entity, so we can access it with "single_mut" method
    let mut velocity = query.single_mut();
    velocity.x = if keyboard.pressed(KeyCode::Left) {
        -1. // -1. is the same as -1_f32
    } else if keyboard.pressed(KeyCode::Right) {
        1.
    } else {
        0.
    };
}
