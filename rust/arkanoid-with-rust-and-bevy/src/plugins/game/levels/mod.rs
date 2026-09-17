mod level1;
mod level2;
mod level3;
mod level4;
mod level5;
mod level6;
mod level7;
mod level8;

pub const LEVELS: [&[&str]; 8] = [
    &level1::LEVEL_MAP,
    &level2::LEVEL_MAP,
    &level3::LEVEL_MAP,
    &level4::LEVEL_MAP,
    &level5::LEVEL_MAP,
    &level6::LEVEL_MAP,
    &level7::LEVEL_MAP,
    &level8::LEVEL_MAP,
];
