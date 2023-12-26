use crate::frame::{Drawable, Frame, COLUMNS_COUNT, ROWS_COUNT};

pub struct Player {
    x_position: usize,
    y_position: usize,
}

impl Player {
    pub fn new() -> Self {
        Self {
            x_position: COLUMNS_COUNT / 2,
            y_position: ROWS_COUNT - 1,
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
}

impl Drawable for Player {
    fn draw(&self, frame: &mut Frame) {
        frame[self.x_position][self.y_position] = "A"
    }
}
