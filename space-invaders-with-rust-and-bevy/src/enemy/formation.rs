use crate::{
    assets::{BASE_SPEED, ENEMY_FORMATION_MEMBERS_MAX},
    resources::WindowSize,
};
use bevy::prelude::{Component, Resource};
use rand::{thread_rng, Rng};

// Component - Enemy Formation (per enemy)
// Each enemy will have its own formation clone
#[derive(Clone, Component)]
pub struct Formation {
    pub start_coordinate: (f32, f32),
    pub radius: (f32, f32),
    pub pivot: (f32, f32),
    pub speed: f32,
    pub angle: f32, // it will be changed per tick
}

// Resource - Formation Factory
#[derive(Default, Resource)]
pub struct FormationFactory {
    // current template of a formation
    // formation will be cloned for all the members of the same formation
    current_template: Option<Formation>,
    // number of enemies in the same formation
    current_members: u8,
}

impl FormationFactory {
    pub fn create_formation(&mut self, window_size: &WindowSize) -> Formation {
        return match (
            &self.current_template,
            self.current_members >= ENEMY_FORMATION_MEMBERS_MAX,
        ) {
            // we have a current template and still can return it as a clone
            (Some(template), false) => {
                self.current_members += 1;

                template.clone()
            }
            // we have to create a new formation (either there is none or we reached the limit of max members)
            (None, _) | (_, true) => {
                self.current_members = 1;
                self.current_template = Some(compute_new_formation(window_size));

                self.current_template.as_ref().unwrap().clone()
            }
        };
    }
}

fn compute_new_formation(window_size: &WindowSize) -> Formation {
    let mut range = thread_rng();

    // compute start coordinates
    let width_span = window_size.width / 2. + 100.;
    let height_span = window_size.height / 2. + 100.;
    let x = if range.gen_bool(0.5) {
        width_span
    } else {
        -width_span
    };
    let y = range.gen_range(-height_span..height_span);
    let start_point = (x, y);

    // compute the center of an ellipse
    let width_span = window_size.width / 4.;
    let height_span = window_size.height / 3. + 50.;
    let pivot = (
        range.gen_range(-width_span..width_span),
        range.gen_range(0.0..height_span),
    );

    // compute the radius
    let radius = (range.gen_range(80.0..150.), 100.);

    // compute a start angle from where the first spawn will occur to the centre of the pivot
    let angle = (y - pivot.1).atan2(x - pivot.0);

    let speed = BASE_SPEED;

    // create formation
    Formation {
        start_coordinate: start_point,
        radius,
        pivot,
        speed,
        angle,
    }
}
