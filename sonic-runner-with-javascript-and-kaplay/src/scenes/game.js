import {
  ANIMATION_JUMP,
  BACKGROUND_SPRITE_WIDTH,
  CITY_SOUND_ID,
  DESTROY_SOUND_ID,
  GAME_OVER_SCENE_ID,
  HURT_SOUND_ID,
  HYPER_RING_SOUND_ID,
  LOCAL_STORAGE_CURRENT_SCORE_KEY,
  MANIA_FONT_ID,
  RING_SOUND_ID,
  TAG_ENEMY,
  TAG_RING,
} from "../constants";
import { createMotobug } from "../entities/motobug";
import { createRing } from "../entities/ring";
import { createSonic } from "../entities/sonic";
import kaplayContext from "../kaplay-context";
import {
  createBackgroundPieces,
  createPlatformPieces,
  switchBackgroundPieces,
  switchPlatformPieces,
} from "./scene-helpers";

// the game speed will get progressivelly faster during play
let gameSpeed = 300;
let score = 0;
let scoreMultiplier = 0;

const game = () => {
  // sets the City sound effect
  const citySoundEffect = kaplayContext.play(CITY_SOUND_ID, {
    volume: 0.2,
    loop: true,
  });
  // sets gravity so we can jump with the Sonic object
  kaplayContext.setGravity(3100);

  // "loop" method runs the given function every X seconds
  kaplayContext.loop(1, () => {
    gameSpeed += 50;
  });

  ////////////////////////////////////////////////////////
  // adding background image
  const backgroundPieces = createBackgroundPieces();

  ////////////////////////////////////////////////////////
  // adding platform image
  const platformsPieces = createPlatformPieces();

  const scoreText = kaplayContext.add([
    kaplayContext.text("SCORE: 0", { font: MANIA_FONT_ID, size: 72 }),
    kaplayContext.pos(20, 20),
  ]);

  ////////////////////////////////////////////////////////
  // adding Sonic image
  const sonic = spawnSonic({ citySoundEffect, scoreText });

  ////////////////////////////////////////////////////////
  // adding Motobug image
  spawnMotobug();

  ////////////////////////////////////////////////////////
  // adding Ring image
  spawnRing();

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
    // after Sonic finished jumping, we need to set the score multiplier back to 0
    if (sonic.isGrounded()) {
      scoreMultiplier = 0;
    }

    switchBackgroundPieces(backgroundPieces);
    switchPlatformPieces(platformsPieces, gameSpeed);
  });
};

const spawnSonic = (gameObjects) => {
  const { citySoundEffect, scoreText } = gameObjects;
  const sonic = createSonic(kaplayContext.vec2(200, 745));
  sonic.setControls(); // custom method defined on the Sonic object
  sonic.setEvents(); // custom method defined on the Sonic object

  // when the Sonic object collides with an enemy
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
      scoreMultiplier++;
      score += 10 * scoreMultiplier;
      scoreText.text = `SCORE: ${score}`;

      // after destroying a motobug update UI as well
      if (scoreMultiplier === 1) {
        sonic.children[0].text = "+10";
      } else if (scoreMultiplier > 1) {
        sonic.children[0].text = `x${scoreMultiplier}`;
      }

      // after showing the text, wait and "hide" it
      kaplayContext.wait(1, () => (sonic.children[0].text = ""));
    } else {
      kaplayContext.play(HURT_SOUND_ID, { volume: 0.5 });

      kaplayContext.setData(LOCAL_STORAGE_CURRENT_SCORE_KEY, score);
      // the second parameter of the "go" method is data we want to pass to the scene we go to
      kaplayContext.go(GAME_OVER_SCENE_ID, citySoundEffect);
    }
  });

  // when the Sonic object collides with a ring
  // "onCollide" method passes the parameter (in this case "ring") to the function
  // the object passed depends on the tag
  sonic.onCollide(TAG_RING, (ring) => {
    // play the sound of collecting a ring
    kaplayContext.play(RING_SOUND_ID, { volume: 0.5 });
    // an enemy object which collided with sonic will be destroyed
    kaplayContext.destroy(ring);
    score++;
    scoreText.text = `SCORE: ${score}`;

    // after collecting a ring update UI as well
    sonic.children[0].text = "+1";
    // after showing the text, wait and "hide" it
    kaplayContext.wait(1, () => (sonic.children[0].text = ""));
  });

  return sonic;
};

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

const spawnRing = () => {
  const ring = createRing(kaplayContext.vec2(1950, 773));
  // "onUpdate" here is executed only on this specific game object
  ring.onUpdate(() => {
    ring.move(-gameSpeed, 0);
  });

  // "onExitScreen" method runs when a game object goes offscreen
  ring.onExitScreen(() => {
    if (ring.pos.x < 0) {
      // "destroy" method removes a game object
      kaplayContext.destroy(ring);
    }
  });

  const waitTime = kaplayContext.rand(0.5, 3);
  // wait random time and then spawn a ring
  kaplayContext.wait(waitTime, spawnRing);
};

export default game;
