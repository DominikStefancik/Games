mod audio_sound;

use std::error::Error;
use std::io;
use std::io::Stdout;
use crossterm::{ExecutableCommand, terminal};
use crossterm::cursor::{Hide, Show};
use crossterm::terminal::{EnterAlternateScreen, LeaveAlternateScreen};
use rusty_audio::Audio;
use audio_sound::AudioSound;

fn main() -> Result<(), Box<dyn Error>> {
    let mut audio = initialise_audio();
    let mut stdout = initialise_terminal().expect("Error while initialising terminal");

    // the sound is played in a separate thread
    audio.play(AudioSound::Startup);

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

fn initialise_terminal() -> Result<Stdout, io::Error> {
    let mut stdout = io::stdout();
    // enable raw mode so we can get a keyboard input as it occurs
    terminal::enable_raw_mode()?;
    // let's enter our alternate screen
    // crossterm package extends the stdout with "execute" method
    stdout.execute(EnterAlternateScreen)?;
    // hide the cursor
    stdout.execute(Hide)?;

    Ok(stdout)
}

fn clean_up_resources(audio: Audio, stdout: &mut Stdout) -> Result<(), io::Error> {
    audio.wait(); // wait until all audio is done playing
    // show the terminal screen
    stdout.execute(Show)?;
    stdout.execute(LeaveAlternateScreen)?;
    terminal::disable_raw_mode()?;

    Ok(())
}