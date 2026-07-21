pub mod camera;
pub mod default;
pub mod food;
pub mod game;
pub mod shared;
pub mod snake;
pub mod window;

pub use camera::CameraPlugin;
pub use default::default_plugin;
pub use food::FoodPlugin;
pub use game::GamePlugin;
pub use shared::SharedPlugin;
pub use snake::SnakePlugin;
pub use window::WindowPlugin;
