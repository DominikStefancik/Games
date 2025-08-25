use std::ops::{Add, Div, Sub};

#[derive(Debug, Copy, Clone, PartialEq)]
pub struct Position<T> {
    pub x: T,
    pub y: T,
}

impl From<Position<f32>> for Position<u32> {
    fn from(value: Position<f32>) -> Self {
        Self {
            x: value.x as u32,
            y: value.y as u32,
        }
    }
}

impl<T> Position<T> {
    pub fn new(x: T, y: T) -> Self {
        Self { x, y }
    }

    pub fn add(&self, other: &Position<T>) -> Self
    where
        T: Add<T, Output = T> + Copy,
    {
        Position {
            x: self.x + other.x,
            y: self.y + other.y,
        }
    }

    pub fn subtract(&self, other: &Position<T>) -> Self
    where
        T: Sub<T, Output = T> + Copy,
    {
        Position {
            x: self.x - other.x,
            y: self.y - other.y,
        }
    }

    pub fn divide(self, value: T) -> Self
    where
        T: Div<T, Output = T> + Copy,
    {
        Position {
            x: self.x / value,
            y: self.y / value,
        }
    }
}
