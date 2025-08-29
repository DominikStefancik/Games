pub struct Board {
    pub rows: u32,
    pub cols: u32,
    pub mines_count: u32,
}

impl Board {
    pub fn small() -> Self {
        Board {
            rows: 10,
            cols: 10,
            mines_count: 10,
        }
    }

    pub fn medium() -> Self {
        Board {
            rows: 16,
            cols: 30,
            mines_count: 99,
        }
    }

    pub fn large() -> Self {
        Board {
            rows: 20,
            cols: 40,
            mines_count: 200,
        }
    }
}
