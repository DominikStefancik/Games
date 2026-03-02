use macroquad::texture::{Texture2D, load_texture};

pub struct Assets {
    pub flag: Texture2D,
    pub mine: Texture2D,
}

impl Assets {
    pub async fn load() -> Self {
        let path = "assets/flag.png";
        let flag = load_texture(path)
            .await
            .unwrap_or_else(|_| panic!("Failed to load flag asset from the path '{}'", path));

        let path = "assets/mine.png";
        let mine = load_texture(path)
            .await
            .unwrap_or_else(|_| panic!("Failed to load mine asset from the path '{}'", path));

        Assets { flag, mine }
    }
}
