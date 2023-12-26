pub enum AudioSound {
    Explode,
    Lose,
    Move,
    Pew,
    Startup,
    Win,
}

impl AsRef<str> for AudioSound {
    fn as_ref(&self) -> &str {
        match self {
            AudioSound::Explode => "Explode",
            AudioSound::Lose => "Lose",
            AudioSound::Move => "Move",
            AudioSound::Pew => "Pew",
            AudioSound::Startup => "Startup",
            AudioSound::Win => "Win",
        }
    }
}
