mod audio_sound;

use std::error::Error;
use rusty_audio::Audio;
use audio_sound::AudioSound;

fn main() -> Result<(), Box<dyn Error>> {
    let mut audio = Audio::new();
    // add all audio sources to the audio manager
    audio.add(AudioSound::Explode, "./audio/explode.wav");
    audio.add(AudioSound::Lose, "./audio/lose.wav");
    audio.add(AudioSound::Move, "./audio/move.wav");
    audio.add(AudioSound::Pew, "./audio/pew.wav");
    audio.add(AudioSound::Startup, "./audio/startup.wav");
    audio.add(AudioSound::Win, "./audio/win.wav");

    // the sound is played in a separate thread
    audio.play(AudioSound::Startup);
    audio.wait(); // wait until all audio is done playing

    Ok(())
}
