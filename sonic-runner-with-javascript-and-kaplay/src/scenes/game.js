import {
  BACKGROUND_SPRITE_SCALE,
  BACKGROUND_SPRITE_WIDTH,
  PLATFORMS_SPRITE_SCALE,
  PLATFORMS_SPRITE_WIDTH,
} from "../constants";
import { createSonic } from "../entities/sonic";
import kaplayContext from "../kaplay-context";
import {
  createBackgroundPieces,
  createPlatformPieces,
  switchBackgroundPieces,
  switchPlatformPieces,
} from "./scene-helpers";

const game = () => {
  // sets gravity so we can jump with the Sonic object
  kaplayContext.setGravity(3100);

  ////////////////////////////////////////////////////////
  // adding background image
  const backgroundPieces = createBackgroundPieces();

  ////////////////////////////////////////////////////////
  // adding platform image
  const platformsPieces = createPlatformPieces();

  ////////////////////////////////////////////////////////
  // adding Sonic image
  const sonic = createSonic(kaplayContext.vec2(200, 745));
  sonic.setControls(); // custom method defined on the Sonic object
  sonic.setEvents(); // custom method defined on the Sonic object

  // the game speed will get progressivelly faster during play
  let gameSpeed = 300;

  // "loop" method runs the given function every X seconds
  kaplayContext.loop(1, () => {
    gameSpeed += 50;
  });

  // add an invisible rectangle which repesents a platformsPiece
  // we add this component so we can detect when the square around the Sonic component
  // collides with the platform
  kaplayContext.add([
    kaplayContext.rect(BACKGROUND_SPRITE_WIDTH, 300),
    // we want to make this rectangle invisible
    kaplayContext.opacity(0),
    // "area" method adds possibility to detect a collision with the platform object
    kaplayContext.area(),
    kaplayContext.pos(0, 832),
    // "body" method makes a game object susceptible to gravity
    // the flag "isStatic" makes the game object static, which means it will not be
    // influenced by gravity
    kaplayContext.body({ isStatic: true }),
  ]);

  // "onUpdate" method will run the function passed as an argument for every frame (60 times per second)
  kaplayContext.onUpdate(() => {
    switchBackgroundPieces(backgroundPieces);
    switchPlatformPieces(platformsPieces, gameSpeed);
  });
};

export default game;
