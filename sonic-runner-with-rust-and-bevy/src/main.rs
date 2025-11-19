use bevy::app::App;

mod plugins;

fn main() {
    App::new().add_plugins(plugins::default::plugin).run();
}
