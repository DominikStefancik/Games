pub const ROWS_COUNT: usize = 60;
pub const COLUMNS_COUNT: usize = 120;

// Vector of vectors of static string slices
pub type Frame = Vec<Vec<&'static str>>;

pub trait Drawable {
    fn draw(&self, frame: &mut Frame);
}

pub fn create_frame() -> Frame {
    // we know the number of columns in advance, so we can optimize the vector with "with_capacity()"
    let mut columns = Vec::with_capacity(COLUMNS_COUNT);

    for _ in 0..COLUMNS_COUNT {
        let mut column = Vec::with_capacity(ROWS_COUNT);

        for _ in 0..ROWS_COUNT {
            column.push(" ")
        }

        columns.push(column);
    }

    columns
}
