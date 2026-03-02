mod helpers;

use crate::constants::{
    BALL_SIZE, BALL_SIZE_HALF, BALL_SPEED, MIDDLE_LINE_WIDTH, RACKET_HEIGHT, RACKET_HEIGHT_HALF,
    RACKET_PADDING, RACKET_WIDTH,
};
use crate::state::helpers::{
    create_ball_square_mesh, create_middle_line_mesh, create_racket_rectangle_mesh, move_racket,
    randomize_velocity,
};
use ggez::{
    event, graphics,
    input::keyboard::KeyCode,
    mint::{Point2, Vector2},
    Context, GameResult,
};

// struct to handle the game loop
pub struct GameState {
    screen_width: f32,
    screen_height: f32,
    player_1: graphics::Mesh,
    player_2: graphics::Mesh,
    ball: graphics::Mesh,
    middle_line: graphics::Mesh,
    player_1_position: Point2<f32>,
    player_2_position: Point2<f32>,
    ball_position: Point2<f32>,
    ball_velocity: Vector2<f32>,
    player_1_score: u16,
    player_2_score: u16,
}

impl GameState {
    // Load/create resources such as images here.
    pub fn new(context: &mut Context) -> Self {
        let (screen_width, screen_height) = context.gfx.drawable_size();
        let (screen_width_half, screen_height_half) = (screen_width / 2., screen_height / 2.);
        let player_1 = create_racket_rectangle_mesh(context);
        let player_2 = create_racket_rectangle_mesh(context);
        let ball = create_ball_square_mesh(context);
        let middle_line = create_middle_line_mesh(&context, screen_height);
        let player_1_position = Point2 {
            x: RACKET_PADDING,
            y: screen_height_half - RACKET_HEIGHT_HALF,
        };
        let player_2_position = Point2 {
            x: screen_width - RACKET_WIDTH - RACKET_PADDING,
            y: screen_height_half - RACKET_HEIGHT_HALF,
        };
        let ball_position = Point2 {
            x: screen_width_half - BALL_SIZE_HALF,
            y: screen_height_half - BALL_SIZE_HALF,
        };
        let mut ball_velocity = Vector2::from([0., 0.]);
        randomize_velocity(&mut ball_velocity, BALL_SPEED, BALL_SPEED);

        GameState {
            screen_width,
            screen_height,
            player_1,
            player_2,
            ball,
            middle_line,
            player_1_position,
            player_2_position,
            ball_position,
            ball_velocity,
            player_1_score: 0,
            player_2_score: 0,
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

        let delta_time = context.time.delta().as_secs_f32();
        self.ball_position.x += self.ball_velocity.x * delta_time;
        self.ball_position.y += self.ball_velocity.y * delta_time;

        // check if ball didn't reach upper or lower boundary
        if self.ball_position.y < 0. {
            self.ball_velocity.y = self.ball_velocity.y.abs();
        } else if self.ball_position.y > self.screen_height - BALL_SIZE {
            self.ball_velocity.y = -self.ball_velocity.y.abs();
        }

        // check if the ball touched one of the rackets
        let ball_touches_player_1 = self.ball_position.x < self.player_1_position.x + RACKET_WIDTH
            && self.ball_position.y + BALL_SIZE > self.player_1_position.y
            && self.ball_position.y < self.player_1_position.y + RACKET_HEIGHT;
        let ball_touches_player_2 = self.ball_position.x > self.player_2_position.x - RACKET_WIDTH
            && self.ball_position.y + BALL_SIZE > self.player_2_position.y
            && self.ball_position.y < self.player_2_position.y + RACKET_HEIGHT;

        if ball_touches_player_1 {
            self.ball_velocity.x = self.ball_velocity.x.abs();
        } else if ball_touches_player_2 {
            self.ball_velocity.x = -self.ball_velocity.x.abs();
        }

        // check if one of the player lost
        if self.ball_position.x < 0. {
            // reset the ball in the middle of the screen
            self.ball_position.x = self.screen_width / 2.;
            self.ball_position.y = self.screen_height / 2.;
            randomize_velocity(&mut self.ball_velocity, BALL_SPEED, BALL_SPEED);
            self.player_2_score += 1;
        } else if self.ball_position.x > self.screen_width {
            // reset the ball in the middle of the screen
            self.ball_position.x = self.screen_width / 2.;
            self.ball_position.y = self.screen_height / 2.;
            randomize_velocity(&mut self.ball_velocity, BALL_SPEED, BALL_SPEED);
            self.player_1_score += 1;
        }

        Ok(())
    }

    fn draw(&mut self, context: &mut Context) -> GameResult {
        let screen_width_half = self.screen_width / 2.;
        let mut canvas = graphics::Canvas::from_frame(context, graphics::Color::BLACK);

        // create Pong rackets on the screen
        canvas.draw(
            &self.player_1,
            graphics::DrawParam::new().dest(self.player_1_position),
        );

        canvas.draw(
            &self.player_2,
            graphics::DrawParam::new().dest(self.player_2_position),
        );

        // create ball on the screen
        canvas.draw(
            &self.ball,
            graphics::DrawParam::new().dest(self.ball_position),
        );

        canvas.draw(
            &self.middle_line,
            graphics::DrawParam::new().dest(Point2 {
                x: screen_width_half - MIDDLE_LINE_WIDTH / 2.,
                y: 0.,
            }),
        );

        let mut score_text = graphics::Text::new(format!(
            "{}    {}",
            self.player_1_score, self.player_2_score
        ));
        score_text.set_scale(45.);
        let score_text_position = Point2 {
            x: screen_width_half - 70.,
            y: 30.,
        };
        canvas.draw(
            &score_text,
            graphics::DrawParam::new().dest(score_text_position),
        );

        canvas.finish(context)?;

        Ok(())
    }
}
