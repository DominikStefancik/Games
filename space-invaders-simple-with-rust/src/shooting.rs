use crate::frame::{Drawable, Frame};
use rusty_time::Timer;
use std::time::Duration;

// represents a single shot at an invader made by a player
pub struct Shot {
    pub x_position: usize,
    pub y_position: usize,
    pub is_exploding: bool,
    move_timer: Timer, // an internal timer to keep track of a shot's movement
}

impl Shot {
    pub fn new(x: usize, y: usize) -> Self {
        Self {
            x_position: x,
            y_position: y,
            is_exploding: false,
            move_timer: Timer::new(Duration::from_millis(50)),
        }
    }

    pub fn update_timer(&mut self, delta: Duration) {
        self.move_timer.tick(delta);

        if self.move_timer.just_finished() && !self.is_exploding {
            if self.y_position > 0 {
                // if we haven't reach a top of the screen, we can move upwards
                self.y_position -= 1;
            }

            self.move_timer.reset();
        }
    }

    pub fn explode(&mut self) {
        self.is_exploding = true;
        self.move_timer = Timer::new(Duration::from_millis(250))
    }

    pub fn is_dead(&self) -> bool {
        // if the shot either exploded or it reached to top position, we need to clean it out
        (self.is_exploding && self.move_timer.just_finished()) || (self.y_position == 0)
    }
}

impl Drawable for Shot {
    fn draw(&self, frame: &mut Frame) {
        frame[self.x_position][self.y_position] = if self.is_exploding { "*" } else { "|" }
    }
}
