import type { RGBValue } from "kaplay";

export const SCREEN = {
  width: 640,
  height: 360,
  background: [0, 0, 0] as RGBValue,
};

export const KEY_CONTROL = {
  enter: "enter",
  left: "left",
  right: "right",
  up: "up",
  space: "space",
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

export const MAP_SPRITE = {
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

export const ENTITY_STATE = {
  drone: {
    patrolRight: "patrolRight",
    patrolLeft: "patrolLeft",
    alert: "alert",
    attack: "attack",
    retreat: "retreat",
  },
};

export const KAPLAY_EVENT = {
  hurt: "hurt",
};

export const CUSTOM_EVENT = {
  explode: "explode",
};

export const TAG = {
  player: "player",
  drone: "drone",
  collider: "collider",
  "sword-hitbox": "sword-hitbox",
  "boss-barrier": "boss-barrier",
};

export const COLLIDER_TYPE = {
  "boss-barrier": "boss-barrier",
  passthrough: "passthrough",
};

export const ROOM_DATA_LAYER_NAME = {
  colliders: "colliders",
  positions: "positions",
  cameras: "cameras",
};

export const POSITION_TAG = {
  player: "player",
  drone: "drone",
};

export const MAP_HORIZONTAL_OFFSET = 160;
export const OFFSCREEN_DISTANCE = 400;
