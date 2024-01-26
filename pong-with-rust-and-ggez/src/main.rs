mod constants;
mod state;

use crate::state::GameState;
use ggez::{event, ContextBuilder, GameResult};

// GameResult is what ggez uses to handle failures or errors
// GameResult<T = ()> = Result<T, GameError>
fn main() -> GameResult {
    // first we need a context to create the screen
    let context_builder = ContextBuilder::new("Rusty Pong", "Dominik");
    let (mut context, event_loop) = context_builder.build().expect("Building a context failed.");
    context.gfx.set_drawable_size(1200., 1000.)?;
    context.gfx.set_window_title("Rust Pong");

    // Create an instance of your event handler.
    // Usually, you should provide it with the Context object to
    // use when setting your game up.
    let game_state = GameState::new(&mut context);

    // start the game loop
    event::run(context, event_loop, game_state);
}
