use crate::{
    assets::{PLAYER_RESPAWN_DELAY, PLAYER_SIZE, SPRITE_SCALE},
    components::{Laser, LaserFromPlayer, Movable, Player, SpriteSize, Velocity},
    resources::{GameTextures, PlayerState, WindowSize},
};
use bevy::time::common_conditions::on_timer;
use bevy::{
    input::ButtonInput,
    prelude::{
        App, Commands, IntoScheduleConfigs, KeyCode, Plugin, PostStartup, Query, Res, ResMut, Time,
        Transform, Update, Vec3, With,
    },
    sprite::Sprite,
};
use std::time::Duration;

// Use player functionality as a plugin
pub struct PlayerPlugin;

// Custom plugin in Bevy has to implement the trait "Plugin" in order to be able to be used
impl Plugin for PlayerPlugin {
    fn build(&self, app: &mut App) {
        app.insert_resource(PlayerState::default())
            .add_systems(PostStartup, player_spawn_system)
            .add_systems(
                Update,
                (
                    player_spawn_system.run_if(on_timer(Duration::from_secs_f32(0.5))),
                    player_keyboard_system,
                    player_fire_system,
                ),
            );
    }
}

fn player_spawn_system(
    mut commands: Commands,
    mut player_state: ResMut<PlayerState>,
    time: Res<Time>,
    game_textures: Res<GameTextures>,
    window_size: Res<WindowSize>,
) {
    let now = time.elapsed_secs_f64();
    let last_shot = player_state.last_shot;

    if !player_state.is_on_stage && (last_shot == -1. || now > last_shot + PLAYER_RESPAWN_DELAY) {
        // position the player at the bottom
        let bottom = -window_size.height / 2.;

        // Add the player
        commands
            .spawn((
                Sprite::from_image(game_textures.player.clone()),
                Transform {
                    translation: Vec3::new(
                        0_f32,
                        bottom + PLAYER_SIZE.1 / 2_f32 * SPRITE_SCALE + 5_f32,
                        10_f32,
                    ),
                    scale: Vec3::new(SPRITE_SCALE, SPRITE_SCALE, 1.),
                    ..Default::default()
                },
            ))
            .insert(Player) // add custom component Player
            .insert(SpriteSize::from(PLAYER_SIZE))
            .insert(Movable { auto_despawn: true })
            .insert(Velocity { x: 1., y: 0. }); // y-position will be the same for the player

        player_state.player_spawned();
    }
}

// system which is changing the velocity of the player
fn player_keyboard_system(
    keyboard_input: Res<ButtonInput<KeyCode>>,
    // here the query only needs movement of a player which we are gonna change
    mut query: Query<&mut Velocity, With<Player>>,
) {
    // we know the query has only one entity, so we can access it with "get_single_mut" method
    if let Ok(mut velocity) = query.single_mut() {
        velocity.x = if keyboard_input.pressed(KeyCode::ArrowLeft) {
            -1. // -1. is the same as -1_f32
        } else if keyboard_input.pressed(KeyCode::ArrowRight) {
            1.
        } else {
            0.
        }
    };
}

fn player_fire_system(
    mut commands: Commands,
    keyboard_input: Res<ButtonInput<KeyCode>>,
    game_textures: Res<GameTextures>,
    query: Query<&Transform, With<Player>>,
) {
    if let Ok(player_transform) = query.single() {
        let (x, y) = (
            player_transform.translation.x,
            player_transform.translation.y,
        );
        // we want to get the position of the edge of the player sprite
        // from the edged the laser will be fired (otherwise it would be from the middle)
        let x_offset = PLAYER_SIZE.0 / 2. * SPRITE_SCALE - 5.;
        let y_offset = 15_f32;

        if keyboard_input.just_pressed(KeyCode::Space) {
            // we want fire two lasers on one key press, the command for rendering both of them
            // will be the same, but just parametrised -> we will use closure for that
            let mut spawn_laser = |x_offset, y_offset| {
                commands
                    .spawn((
                        Sprite::from_image(game_textures.player_laser.clone()),
                        Transform {
                            translation: Vec3::new(x + x_offset, y + y_offset, 0.),
                            scale: Vec3::new(SPRITE_SCALE, SPRITE_SCALE, 1.),
                            ..Default::default()
                        },
                    ))
                    .insert(Movable { auto_despawn: true })
                    // insert a custom component for the laser which will be its velocity
                    // the laser will go up, so only y-position will change;
                    .insert(Velocity { x: 0., y: 1. })
                    .insert(Laser)
                    .insert(LaserFromPlayer)
                    .insert(SpriteSize::from(PLAYER_SIZE));
            };

            spawn_laser(x_offset, y_offset);
            spawn_laser(-x_offset, y_offset);
        };
    };
}
