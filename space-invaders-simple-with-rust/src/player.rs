use crate::frame::{Drawable, Frame, COLUMNS_COUNT, ROWS_COUNT};
use crate::invaders::InvadersArmy;
use crate::shooting::Shot;
use std::time::Duration;

pub struct Player {
    x_position: usize,
    y_position: usize,
    shots: Vec<Shot>,
}

const MAX_SHOTS_COUNT: usize = 3;

impl Player {
    pub fn new() -> Self {
        Self {
            x_position: COLUMNS_COUNT / 2,
            y_position: ROWS_COUNT - 1,
            shots: Vec::new(),
        }
    }

    pub fn move_left(&mut self) {
        if self.x_position > 0 {
            self.x_position -= 1;
        }
    }

    pub fn move_right(&mut self) {
        if self.x_position < COLUMNS_COUNT - 1 {
            self.x_position += 1;
        }
    }

    // there is a limited number of shots we can make at the same time
    // the return value says if a shot was produced or not
    pub fn shoot(&mut self) -> bool {
        if self.shots.len() < MAX_SHOTS_COUNT {
            self.shots
                .push(Shot::new(self.x_position, self.y_position - 1));

            true
        } else {
            false
        }
    }

    pub fn update_shots_timer(&mut self, delta: Duration) {
        // iterate over shots in a mutable way so we can change them
        for shot in self.shots.iter_mut() {
            shot.update_timer(delta);
        }

        // the method "retain" keeps or removes items in/from a vector depending on the return value from a closure
        self.shots.retain(|shot| !shot.is_dead())
    }

    pub fn invader_was_hit(&mut self, invaders_army: &mut InvadersArmy) -> bool {
        let mut invader_was_hit = false;

        for shot in self.shots.iter_mut() {
            if !shot.is_exploding {
                if invaders_army.kill_invader_at(shot.x_position, shot.y_position) {
                    invader_was_hit = true;
                    shot.explode(); // if we hit an invader, the shot has to explode
                }
            }
        }

        invader_was_hit
    }
}

impl Drawable for Player {
    fn draw(&self, frame: &mut Frame) {
        // draw a player itself
        frame[self.x_position][self.y_position] = "A";

        // draw all shots a player shot
        for shot in self.shots.iter() {
            shot.draw(frame);
        }
    }
}
