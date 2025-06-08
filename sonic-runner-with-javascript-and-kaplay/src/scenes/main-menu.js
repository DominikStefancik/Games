import {
  BACKGROUND_SPRITE_SCALE,
  BACKGROUND_SPRITE_WIDTH,
  CHEMICAL_BACKGROUND_SPRITE_ID,
  INSTRUCTIONS_FONT_SIZE,
  MANIA_FONT_ID,
  PLATFORMS_SPRITE_ID,
  PLATFORMS_SPRITE_SCALE,
  PLATFORMS_SPRITE_WIDTH,
  TITLE_FONT_SIZE,
} from "../constants";
import { createSonic } from "../entities/sonic";
import kaplayContext from "../kaplay-context";

const mainMenu = () => {
  // kaplay checks in the local storage for the best score
  if (!kaplayContext.getData("best-score")) {
    kaplayContext.setData("best-score", 0);
  }

  // the "jumpKey" button is defined in the kaplay context
  kaplayContext.onButtonPress("jumpKey", () => kaplayContext.go("game"));

  ////////////////////////////////////////////////////////
  // adding background image
  const backgroundPieces = [
    // adds a game object into a scene
    // the game object is created from array of components
    // adding components to a game object allows us to add additional components dependent on them
    // (you can think about adding components like mutating the game object and giving it ability to have
    // additional components)
    kaplayContext.add([
      // "sprite" method attaches and renders a sprite to a game object
      kaplayContext.sprite(CHEMICAL_BACKGROUND_SPRITE_ID),
      // "pos" method allows us to set a position of a game object
      kaplayContext.pos(0, 0),
      // "scale" method allows us to scale the game object (in our case the background image)
      kaplayContext.scale(BACKGROUND_SPRITE_SCALE),
      // "opacity" method sets the opacity of the game object
      kaplayContext.opacity(0.8),
    ]),
    // puting the same background image twice allows us to create an effect if infitite background scroll
    kaplayContext.add([
      kaplayContext.sprite(CHEMICAL_BACKGROUND_SPRITE_ID),
      // we want to position the "second" background image right after the first one
      // but since we scaled the image twice, we have to add BACKGROUND_SPRITE_WIDTH * 2
      kaplayContext.pos(BACKGROUND_SPRITE_WIDTH * BACKGROUND_SPRITE_SCALE, 0),
      kaplayContext.scale(BACKGROUND_SPRITE_SCALE),
      kaplayContext.opacity(0.8),
    ]),
  ];

  ////////////////////////////////////////////////////////
  // adding platform image
  const platformsPieces = [
    kaplayContext.add([
      kaplayContext.sprite(PLATFORMS_SPRITE_ID),
      kaplayContext.pos(0, 450),
      kaplayContext.scale(PLATFORMS_SPRITE_SCALE),
    ]),
    // puting the same background image twice allows us to create an effect if infitite background scroll
    kaplayContext.add([
      kaplayContext.sprite(PLATFORMS_SPRITE_ID),
      // we want to position the "second" platforms image right after the first one
      // but since we scaled the image 4x, we have to add PLATFORMS_SPRITE_WIDTH * 4
      kaplayContext.pos(PLATFORMS_SPRITE_WIDTH * PLATFORMS_SPRITE_SCALE, 450),
      kaplayContext.scale(PLATFORMS_SPRITE_SCALE),
    ]),
  ];

  ////////////////////////////////////////////////////////
  // adding text
  kaplayContext.add([
    kaplayContext.text("SONIC RING RUN", {
      font: MANIA_FONT_ID,
      size: TITLE_FONT_SIZE,
    }),
    // "center" method returns the center of the canvas
    kaplayContext.pos(kaplayContext.center().x, 200),
    kaplayContext.anchor("center"),
  ]);

  kaplayContext.add([
    kaplayContext.text("Press Space/Click/Touch to Play", {
      font: MANIA_FONT_ID,
      size: INSTRUCTIONS_FONT_SIZE,
    }),
    // "center" method returns the center of the canvas
    kaplayContext.pos(kaplayContext.center().x, kaplayContext.center().y - 200),
    kaplayContext.anchor("center"),
  ]);

  ////////////////////////////////////////////////////////
  // adding Sonic image
  createSonic(kaplayContext.vec2(200, 745));

  // "onUpdate" method will run the function passed as an argument for every frame (60 times per second)
  kaplayContext.onUpdate(() => {
    // the "second" background piece has gone far to left, outside of the bounds of a canvas
    // we can take the "first" first background piece and put it behind
    if (backgroundPieces[1].pos.x < 0) {
      // what we do here is to replace the order of the background components
      // the "first" component will become the "second" and the "second" will become the "first"
      // this way we will achieve the effect of an infinite scrolling background
      backgroundPieces[0].moveTo(
        backgroundPieces[1].pos.x +
          BACKGROUND_SPRITE_WIDTH * BACKGROUND_SPRITE_SCALE,
        0,
      );
      backgroundPieces.push(backgroundPieces.shift());
    }

    // "move" method allows you to move a game object according to a specific velocity
    backgroundPieces[0].move(-100, 0);
    backgroundPieces[1].moveTo(
      backgroundPieces[0].pos.x +
        BACKGROUND_SPRITE_WIDTH * BACKGROUND_SPRITE_SCALE,
      0,
    );

    // the same scrolling effect for platforms as we have for the background image
    if (platformsPieces[1].pos.x < 0) {
      platformsPieces[0].moveTo(
        platformsPieces[1].pos.x +
          PLATFORMS_SPRITE_WIDTH * PLATFORMS_SPRITE_SCALE,
        450,
      );
      platformsPieces.push(platformsPieces.shift());
    }

    // "move" method allows you to move a game object according to a specific velocity
    platformsPieces[0].move(-2000, 0);
    platformsPieces[1].moveTo(
      platformsPieces[0].pos.x +
        PLATFORMS_SPRITE_WIDTH * PLATFORMS_SPRITE_SCALE,
      450,
    );
  });
};

export default mainMenu;
