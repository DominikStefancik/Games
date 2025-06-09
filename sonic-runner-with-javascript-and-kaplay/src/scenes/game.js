import {
  ANIMATION_JUMP,
  BACKGROUND_SPRITE_WIDTH,
  DESTROY_SOUND_ID,
  GAME_OVER_SCENE_ID,
  HURT_SOUND_ID,
  HYPER_RING_SOUND_ID,
  TAG_ENEMY,
} from "../constants";
import { createMotobug } from "../entities/motobug";
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

  // when the Sonic object collides with the enemy
  // "onCollide" method passes the parameter (in this case "enemy") to the function
  // the object passed depends on the tag
  sonic.onCollide(TAG_ENEMY, (enemy) => {
    if (!sonic.isGrounded()) {
      // play the sound of destroying the enemy
      kaplayContext.play(DESTROY_SOUND_ID, { volume: 0.5 });
      kaplayContext.play(HYPER_RING_SOUND_ID, { volume: 0.5 });
      // an enemy object which collided with sonic will be destroyed
      kaplayContext.destroy(enemy);
      sonic.play(ANIMATION_JUMP);
      sonic.jump();
    } else {
      kaplayContext.play(HURT_SOUND_ID, { volume: 0.5 });
      kaplayContext.go(GAME_OVER_SCENE_ID);
    }
  });

  // the game speed will get progressivelly faster during play
  let gameSpeed = 300;

  // "loop" method runs the given function every X seconds
  kaplayContext.loop(1, () => {
    gameSpeed += 50;
  });

  const spawnMotobug = () => {
    const motoBug = createMotobug(kaplayContext.vec2(1950, 773));
    // "onUpdate" here is executed only on this specific game object
    motoBug.onUpdate(() => {
      if (gameSpeed < 3000) {
        // at the beginning, the Motobug game object moves faster than the platform,
        motoBug.move(-(gameSpeed + 300), 0);
      }

      // the Motobug game object moves with the same speed as the platform,
      // which makes him look stationary
      motoBug.move(-gameSpeed, 0);
    });

    // "onExitScreen" method runs when a game object goes offscreen
    motoBug.onExitScreen(() => {
      if (motoBug.pos.x < 0) {
        // "destroy" method removes a game object
        kaplayContext.destroy(motoBug);
      }
    });

    const waitTime = kaplayContext.rand(0.5, 2.5);
    // wait random time and then spawn a motobug
    kaplayContext.wait(waitTime, spawnMotobug);
  };
  spawnMotobug();

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
