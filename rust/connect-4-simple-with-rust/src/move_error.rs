use std::fmt;

#[derive(Debug)]
pub enum MoveError {
    InvalidColumn,
    ColumnFull,
    GameFinished,
}

impl fmt::Display for MoveError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            MoveError::ColumnFull => write!(f, "Column is full"),
            MoveError::InvalidColumn => write!(f, "Column must be between 1 and 7"),
            MoveError::GameFinished => write!(f, "The game is already finished"),
        }
    }
}
