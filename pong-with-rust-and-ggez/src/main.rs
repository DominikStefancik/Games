mod constants;

use crate::constants::{BALL_SIZE, RACKET_HEIGHT, RACKET_WIDTH, RACKET_WIDTH_HALF};
use ggez::{event, graphics, mint::Point2, Context, ContextBuilder, GameResult};

// struct to handle the game loop
struct GameState {
    player_1_position: Point2<f32>,
    player_2_position: Point2<f32>,
    ball_position: Point2<f32>,
}

impl GameState {
    // Load/create resources such as images here.
    fn new(context: &mut Context) -> Self {
        let (screen_width, screen_height) = context.gfx.drawable_size();
        let (screen_width_half, screen_height_half) = (screen_width / 2., screen_height / 2.);

        GameState {
            player_1_position: Point2 {
                x: RACKET_WIDTH_HALF,
                y: screen_height_half,
            },
            player_2_position: Point2 {
                x: screen_width - RACKET_WIDTH - RACKET_WIDTH_HALF,
                y: screen_height_half,
            },
            ball_position: Point2 {
                x: screen_width_half,
                y: screen_height_half,
            },
        }
    }
}

impl event::EventHandler for GameState {
    fn update(&mut self, _ctx: &mut Context) -> GameResult {
        Ok(())
    }

    fn draw(&mut self, context: &mut Context) -> GameResult {
        let mut canvas = graphics::Canvas::from_frame(context, graphics::Color::BLACK);

        // create Pong rackets on the screen
        let racket_rectangle_mesh = create_racket_rectangle_mesh(context);
        canvas.draw(
            &racket_rectangle_mesh,
            graphics::DrawParam::new().dest(self.player_1_position),
        );

        let racket_rectangle_mesh = create_racket_rectangle_mesh(context);
        canvas.draw(
            &racket_rectangle_mesh,
            graphics::DrawParam::new().dest(self.player_2_position),
        );

        // create ball on the screen
        let ball_rectangle_mesh = create_ball_square_mesh(context);
        canvas.draw(
            &ball_rectangle_mesh,
            graphics::DrawParam::new().dest(self.ball_position),
        );

        canvas.finish(context)?;

        Ok(())
    }
}

// GameResult is what ggez uses to handle failures or errors
// GameResult<T = ()> = Result<T, GameError>
fn main() -> GameResult {
    // first we need a context to create the screen
    let context_builder = ContextBuilder::new("Rusty Pong", "Dominik");
    let (mut context, event_loop) = context_builder.build().expect("Building a context failed.");
    context.gfx.set_window_title("Rust Pong");

    // Create an instance of your event handler.
    // Usually, you should provide it with the Context object to
    // use when setting your game up.
    let game_state = GameState::new(&mut context);

    // start the game loop
    event::run(context, event_loop, game_state);
}

fn create_racket_rectangle_mesh(context: &Context) -> graphics::Mesh {
    // define a rectangle boundaries
    let racket_rectangle = graphics::Rect::new(0., 0., RACKET_WIDTH, RACKET_HEIGHT);

    // to draw a rectangle on the screen, we need to generate a mesh
    graphics::Mesh::new_rectangle(
        context,
        graphics::DrawMode::fill(),
        racket_rectangle,
        graphics::Color::WHITE,
    )
    .expect("Creating a rectangle mesh failed.")
}

fn create_ball_square_mesh(context: &Context) -> graphics::Mesh {
    // define a rectangle boundaries
    let racket_rectangle = graphics::Rect::new(0., 0., BALL_SIZE, BALL_SIZE);

    // to draw a rectangle on the screen, we need to generate a mesh
    graphics::Mesh::new_rectangle(
        context,
        graphics::DrawMode::fill(),
        racket_rectangle,
        graphics::Color::WHITE,
    )
    .expect("Creating a rectangle mesh failed.")
}
