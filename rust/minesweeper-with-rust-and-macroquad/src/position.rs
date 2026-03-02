use std::ops::{Add, Div, Sub};

#[derive(Debug, Copy, Clone, PartialEq)]
pub struct Position<T> {
    pub x: T,
    pub y: T,
}

impl From<Position<f32>> for Position<i32> {
    fn from(value: Position<f32>) -> Self {
        Self {
            x: value.x as i32,
            y: value.y as i32,
        }
    }
}

impl<T> Position<T> {
    pub const fn new(x: T, y: T) -> Self {
        Self { x, y }
    }

    pub fn add(&self, other: &Position<T>) -> Self
    // we need to add a WHERE part in which we specify that the type can perform a addition
    where
        T: Add<T, Output = T> + Copy,
    {
        Position {
            x: self.x + other.x,
            y: self.y + other.y,
        }
    }

    pub fn subtract(&self, other: &Position<T>) -> Self
    // we need to add a WHERE part in which we specify that the type can perform a subtraction
    where
        T: Sub<T, Output = T> + Copy,
    {
        Position {
            x: self.x - other.x,
            y: self.y - other.y,
        }
    }

    pub fn divide(self, value: T) -> Self
    // we need to add a WHERE part in which we specify that the type can perform a division
    where
        T: Div<T, Output = T> + Copy,
    {
        Position {
            x: self.x / value,
            y: self.y / value,
        }
    }
}
