use bevy::{
    camera::Camera2d,
    ecs::{
        query::With,
        system::{Commands, Res, ResMut, Single},
    },
    math::Vec3,
    time::Time,
    transform::components::Transform,
};

use crate::plugins::camera::ScreenShake;

pub fn spawn_camera(mut commands: Commands) {
    commands.spawn(Camera2d);
}
/*
 * Because the timer starts pre-finished (we called t.finish() in "insert_resource"),
 * this system runs every frame doing nothing until a death occurs and shake.0.reset() is called.
 */
pub fn apply_screenshake(
    time: Res<Time>,
    mut camera_transform: Single<&mut Transform, With<Camera2d>>,
    mut screenshake: ResMut<ScreenShake>,
) {
    screenshake.0.tick(time.delta());

    if screenshake.0.is_finished() {
        if camera_transform.translation != Vec3::ZERO {
            camera_transform.translation = Vec3::ZERO;
        }
    } else {
        /*
         * "screenshake.0.fraction()" goes from 0.0 to 1.0 as time passes, so 1.0 - fraction() starts at 1.0 and decays to 0.0.
         * Multiplying by 10.0 gives a starting intensity of 10 pixels that eases to zero.
         * When finished, the camera is snapped back to Vec3::ZERO
         */
        let intensity = 10. * (1. - screenshake.0.fraction());
        camera_transform.translation = Vec3::new(
            rand::random::<f32>() * 2. * intensity - intensity,
            rand::random::<f32>() * 2. * intensity - intensity,
            0.,
        );
    }
}

pub fn reset_screenshake_timer(mut screenshake: ResMut<ScreenShake>) {
    screenshake.0.reset();
}
