mod helpers;

use crate::constants::{BALL_SIZE_HALF, RACKET_HEIGHT_HALF, RACKET_WIDTH, RACKET_WIDTH_HALF};
use crate::state::helpers::{create_ball_square_mesh, create_racket_rectangle_mesh, move_racket};
use ggez::{event, graphics, input::keyboard::KeyCode, mint::Point2, Context, GameResult};

// struct to handle the game loop
pub struct GameState {
    screen_width: f32,
    screen_height: f32,
    player_1_position: Point2<f32>,
    player_2_position: Point2<f32>,
    ball_position: Point2<f32>,
}

impl GameState {
    // Load/create resources such as images here.
    pub fn new(context: &mut Context) -> Self {
        let (screen_width, screen_height) = context.gfx.drawable_size();
        let (screen_width_half, screen_height_half) = (screen_width / 2., screen_height / 2.);

        GameState {
            screen_width,
            screen_height,
            player_1_position: Point2 {
                x: RACKET_WIDTH_HALF,
                y: screen_height_half - RACKET_HEIGHT_HALF,
            },
            player_2_position: Point2 {
                x: screen_width - RACKET_WIDTH - RACKET_WIDTH_HALF,
                y: screen_height_half - RACKET_HEIGHT_HALF,
            },
            ball_position: Point2 {
                x: screen_width_half - BALL_SIZE_HALF,
                y: screen_height_half - BALL_SIZE_HALF,
            },
        }
    }
}

impl event::EventHandler for GameState {
    fn update(&mut self, context: &mut Context) -> GameResult {
        move_racket(
            context,
            self.screen_height,
            &mut self.player_1_position,
            KeyCode::W,
            -1.,
        );
        move_racket(
            context,
            self.screen_height,
            &mut self.player_1_position,
            KeyCode::S,
            1.,
        );
        move_racket(
            context,
            self.screen_height,
            &mut self.player_2_position,
            KeyCode::Up,
            -1.,
        );
        move_racket(
            context,
            self.screen_height,
            &mut self.player_2_position,
            KeyCode::Down,
            1.,
        );

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