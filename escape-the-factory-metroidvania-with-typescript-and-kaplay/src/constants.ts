import type { RGBValue } from "kaplay";

export const SCREEN = {
  width: 640,
  height: 360,
  background: [0, 0, 0] as RGBValue,
};

export const FONT = {
  glyphmesss: "glyphmesss",
};

export const SOUND = {
  notify: "notify",
  boom: "boom",
  health: "health",
  flamethrower: "flamethrower",
};

export const SCENE = {
  intro: "intro",
  room1: "room1",
  room2: "room2",
};

export const ENTITY_SPRITE = {
  player: "player",
  drone: "drone",
  bossBurner: "bossBurner",
};

export const ATLAS_SPRITE = {
  healthbar: "healthbar",
  cartridge: "cartridge",
};

export const TILESET_SPRITE = {
  tileset: "tileset",
  background: "background",
};

export const ANIMATION = {
  player: {
    idle: "idle",
    run: "run",
    jump: "jump",
    fall: "fall",
    attack: "attack",
    explode: "explode",
  },
  drone: {
    flying: "flying",
    attack: "attack",
    explode: "explode",
  },
  bossBurner: {
    idle: "idle",
    run: "run",
    openFire: "openFire",
    fire: "fire",
    shutFire: "shutFire",
    explode: "explode",
  },
  cartridge: {
    default: "default",
  },
};
