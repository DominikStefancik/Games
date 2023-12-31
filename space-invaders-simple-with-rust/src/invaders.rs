use crate::frame::{Drawable, Frame, COLUMNS_COUNT, ROWS_COUNT};
use rusty_time::Timer;
use std::cmp::max;
use std::time::Duration;

pub struct Invader {
    x_position: usize,
    y_position: usize,
}

pub struct InvadersArmy {
    army: Vec<Invader>,
    move_timer: Timer,
    direction: InvadersDirection,
}

#[derive(PartialEq)]
enum InvadersDirection {
    RIGHT,
    LEFT,
}

impl Invader {
    pub fn new(x: usize, y: usize) -> Self {
        Self {
            x_position: x,
            y_position: y,
        }
    }
}
impl InvadersArmy {
    pub fn new() -> Self {
        let mut army = Vec::new();

        for x in 0..COLUMNS_COUNT {
            for y in 0..ROWS_COUNT {
                if (x > 1)
                    && (x < COLUMNS_COUNT - 2)
                    && (y > 0)
                    && (y < 9)
                    && (x % 2 == 0)
                    && (y % 2 == 0)
                {
                    army.push(Invader::new(x, y))
                }
            }
        }

        Self {
            army,
            move_timer: Timer::new(Duration::from_millis(2000)), // 2 seconds
            direction: InvadersDirection::RIGHT,
        }
    }

    // as a return value is a Boolean flag which indicates it the entire army moved
    pub fn update_timer(&mut self, delta: Duration) -> bool {
        self.move_timer.tick(delta);

        if self.move_timer.finished() {
            self.move_timer.reset();
            let mut move_downwards = false;

            if self.direction == InvadersDirection::LEFT {
                let min_x = self
                    .army
                    .iter()
                    .map(|invader| invader.x_position)
                    .min()
                    .unwrap_or(0); // if the vector is empty, we return 0

                if min_x == 0 {
                    // we have reached the most left position -> we are moving down
                    move_downwards = true;
                    self.direction = InvadersDirection::RIGHT;
                }
            } else {
                let max_x = self
                    .army
                    .iter()
                    .map(|invader| invader.x_position)
                    .max()
                    .unwrap_or(0);

                if max_x == COLUMNS_COUNT - 1 {
                    move_downwards = true;
                    self.direction = InvadersDirection::LEFT;
                }
            }

            if move_downwards {
                // whenever we move downwards, we are gonna increase the speed if the movement
                let new_duration = max(self.move_timer.duration().as_millis() - 250, 250);
                self.move_timer = Timer::new(Duration::from_millis(new_duration as u64));

                // move all invaders downwards
                for invader in self.army.iter_mut() {
                    invader.y_position += 1;
                }
            } else {
                for invader in self.army.iter_mut() {
                    if self.direction == InvadersDirection::RIGHT {
                        invader.x_position += 1
                    } else {
                        invader.x_position -= 1
                    }
                }
            }

            return true;
        }

        false
    }
}

impl Drawable for InvadersArmy {
    fn draw(&self, frame: &mut Frame) {
        for invader in self.army.iter() {
            frame[invader.x_position][invader.y_position] =
                // half of the time we render invaders as one character and another half as a different character
                if self.move_timer.remaining().as_secs_f32() / self.move_timer.duration().as_secs_f32() > 0.5 {
                    "x"
                } else {
                    "+"
                };
        }
    }
}
