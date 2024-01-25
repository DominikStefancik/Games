use crate::constants::{BALL_SIZE, RACKET_HEIGHT, RACKET_SPEED, RACKET_WIDTH};
use ggez::{
    graphics,
    input::keyboard::KeyCode,
    mint::{Point2, Vector2},
    Context,
};
use rand::Rng;

pub fn create_racket_rectangle_mesh(context: &Context) -> graphics::Mesh {
    // define a rectangle boundaries
    let racket_rectangle = graphics::Rect::new(0., 0., RACKET_WIDTH, RACKET_HEIGHT);

    // to draw a rectangle on the screen, we need to generate a mesh
    create_rectangle_mesh(context, racket_rectangle)
}

pub fn create_ball_square_mesh(context: &Context) -> graphics::Mesh {
    // define a rectangle boundaries
    let ball_squqre = graphics::Rect::new(0., 0., BALL_SIZE, BALL_SIZE);

    // to draw a rectangle on the screen, we need to generate a mesh
    create_rectangle_mesh(context, ball_squqre)
}

fn create_rectangle_mesh(context: &Context, rectangle: graphics::Rect) -> graphics::Mesh {
    graphics::Mesh::new_rectangle(
        context,
        graphics::DrawMode::fill(),
        rectangle,
        graphics::Color::WHITE,
    )
    .expect("Creating a rectangle mesh failed.")
}

pub fn move_racket(
    context: &Context,
    screen_height: f32,
    position: &mut Point2<f32>,
    key_code: KeyCode,
    direction: f32,
) {
    let delta_time = context.time.delta().as_secs_f32();

    if context.keyboard.is_key_pressed(key_code) {
        position.y += direction * RACKET_SPEED * delta_time;
    }

    clamp(&mut position.y, 0., screen_height - RACKET_HEIGHT);
}

// function used to keep drawn objects inside of the screen
fn clamp(value: &mut f32, low: f32, high: f32) {
    if *value < low {
        *value = low;
    } else if *value > high {
        *value = high;
    }
}

pub fn randomize_velocity(vector: &mut Vector2<f32>, x: f32, y: f32) {
    let mut random_generator = rand::thread_rng();
    vector.x = match random_generator.gen_bool(0.5) {
        true => x,
        false => -x,
    };
    vector.y = match random_generator.gen_bool(0.5) {
        true => y,
        false => -y,
    }
}
