use crossterm::{cursor, event, terminal, ExecutableCommand};
use rusty_audio::Audio;
use std::time::Instant;
use std::{error::Error, io, sync::mpsc, thread, time::Duration};

use space_invaders_simple_with_rust::{
    audio_sound::AudioSound,
    frame::{create_frame, Drawable},
    invaders::InvadersArmy,
    player::Player,
    render,
};

fn main() -> Result<(), Box<dyn Error>> {
    let mut audio = initialise_audio();
    let mut stdout = initialise_terminal().expect("Error while initialising terminal");

    // the sound is played in a separate thread
    audio.play(AudioSound::Startup);

    // render a frame in a separate thread
    let (render_transmitter, render_receiver) = mpsc::channel();
    let render_handler = thread::spawn(move || {
        let mut last_frame = create_frame();
        // we are in a different thread than main, so we need a separate reference to Stdout
        let mut stdout = io::stdout();

        render::render_frame(&mut stdout, &last_frame, &last_frame, true);

        // incremental updates
        loop {
            // the method "recv()" either returns a current frame or if the channel was closed, it returns an error
            let current_frame = match render_receiver.recv() {
                Ok(frame) => frame,
                Err(_) => break, // breaking out of the render loop will shutdown our channel thread
            };
            render::render_frame(&mut stdout, &last_frame, &current_frame, false);
            last_frame = current_frame;
        }
    });

    let mut player = Player::new();
    let mut instant = Instant::now();
    let mut invaders = InvadersArmy::new();
    // we name the loop, because we want to reference it so we can exit it anywhere from inside the loop
    'gameloop: loop {
        // Per frame initialisation
        let delta = instant.elapsed();
        instant = Instant::now();
        let mut current_frame = create_frame();

        // we are polling from input events
        // poll() function takes a duration time we want to wait after an event happened
        while event::poll(Duration::default())? {
            // we are only interested in KeyEvents
            if let event::Event::Key(key_event) = event::read()? {
                match key_event.code {
                    event::KeyCode::Esc | event::KeyCode::Char('q') => {
                        // we break out of the game before it finishes, so we lose
                        audio.play(AudioSound::Lose);
                        break 'gameloop;
                    }
                    event::KeyCode::Left => player.move_left(),
                    event::KeyCode::Right => player.move_right(),
                    event::KeyCode::Char(' ') | event::KeyCode::Enter => {
                        if player.shoot() {
                            audio.play(AudioSound::Pew);
                        }
                    }
                    _ => {}
                }
            }
        }

        // Timer updates
        player.update_shots_timer(delta);

        if invaders.update_timer(delta) {
            audio.play(AudioSound::Move);
        }

        if player.invader_was_hit(&mut invaders) {
            audio.play(AudioSound::Explode)
        }

        // Draw and render everything which needs to be drawn
        let drawables: Vec<&dyn Drawable> = vec![&player, &invaders];

        for drawable in drawables {
            drawable.draw(&mut current_frame);
        }

        // whatever result, including an error, will silently be ignored
        let _ = render_transmitter.send(current_frame);
        // since the "gameloop" is much faster than rendering the frame, we artificially include sleep
        thread::sleep(Duration::from_millis(1));

        // Decide whether we won or lost
        if invaders.are_all_killed() {
            audio.play(AudioSound::Win);
            break 'gameloop;
        }

        if invaders.reached_bottom() {
            audio.play(AudioSound::Lose);
            break 'gameloop;
        }
    }

    // shutdown the sending channel which will trigger an exit of the thread in which the rendering is happening
    drop(render_transmitter);
    // we wait until the thread actually joins
    render_handler.join().unwrap();

    clean_up_resources(audio, &mut stdout)?;

    Ok(())
}

fn initialise_audio() -> Audio {
    let mut audio = Audio::new();
    // add all audio sources to the audio manager
    audio.add(AudioSound::Explode, "./audio/explode.wav");
    audio.add(AudioSound::Lose, "./audio/lose.wav");
    audio.add(AudioSound::Move, "./audio/move.wav");
    audio.add(AudioSound::Pew, "./audio/pew.wav");
    audio.add(AudioSound::Startup, "./audio/startup.wav");
    audio.add(AudioSound::Win, "./audio/win.wav");

    audio
}

fn initialise_terminal() -> Result<io::Stdout, io::Error> {
    let mut stdout = io::stdout();
    // enable raw mode so we can get a keyboard input as it occurs
    terminal::enable_raw_mode()?;
    // let's enter our alternate screen
    // crossterm package extends the stdout with "execute" method
    stdout.execute(terminal::EnterAlternateScreen)?;
    // hide the cursor
    stdout.execute(cursor::Hide)?;

    Ok(stdout)
}

fn clean_up_resources(audio: Audio, stdout: &mut io::Stdout) -> Result<(), io::Error> {
    // wait until all audio is done playing
    audio.wait();
    // show the terminal screen
    stdout.execute(cursor::Show)?;
    stdout.execute(terminal::LeaveAlternateScreen)?;
    terminal::disable_raw_mode()?;

    Ok(())
}
